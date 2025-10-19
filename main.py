#!/usr/bin/env python3
"""
Code Cartographer - Main Script

This is the command-line interface for Code Cartographer.
It orchestrates the parser service (tree-sitter) and the AI service (OpenAI)
to provide intelligent code analysis.

Usage:
    Single file:    python main.py path/to/code/file.py
    Batch mode:     python main.py --batch path/to/project
    With exclude:   python main.py --batch . --exclude "tests,docs"
    Visualize:      python main.py --visualize . --output graph.html
    With AI arch:   python main.py --visualize . --architecture
"""

import sys
import os
import argparse
from pathlib import Path
from tqdm import tqdm
from services.parser_service import analyze_code
from services.ai_service import get_ai_summary_sync, analyze_project_architecture
from services.batch_analyzer import (
    analyze_project, 
    save_analysis_cache,
    get_project_summary
)
from services.dependency_analyzer import (
    analyze_dependencies,
    get_dependency_summary
)
from services.visualization_service import (
    generate_dependency_graph,
    export_graph_html,
    export_graph_image,
    export_graph_json,
    create_statistics_visualization
)


def print_header():
    """Print a nice header for the output."""
    print("\n" + "=" * 80)
    print("CODE CARTOGRAPHER - AI-Powered Repository Navigator".center(80))
    print("=" * 80 + "\n")


def print_analysis_header(file_path: str):
    """Print the file being analyzed."""
    print(f"📄 Analyzing: {file_path}")
    print("-" * 80 + "\n")


def analyze_single_file_mode(file_path: str):
    """Analyze a single file with AI summary."""
    try:
        # Print headers
        print_header()
        print_analysis_header(file_path)
        
        # Step 1: Parse the code structure
        print("🔍 Step 1/3: Parsing code structure with tree-sitter...")
        analysis_results = analyze_code(file_path)
        
        # Print quick stats
        print(f"   ✓ Found {len(analysis_results['imports'])} imports")
        print(f"   ✓ Found {len(analysis_results['definitions'])} function definitions")
        print(f"   ✓ Found {len(analysis_results['calls'])} function calls\n")
        
        # Step 2: Read the file content
        print("📖 Step 2/3: Reading file content...")
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        print(f"   ✓ Read {len(code_content)} characters\n")
        
        # Step 3: Generate AI summary
        print("🤖 Step 3/3: Generating AI-powered summary...")
        print("   (This may take 10-30 seconds...)\n")
        summary = get_ai_summary_sync(file_path, code_content, analysis_results)
        
        # Print the final summary
        print("=" * 80)
        print("ANALYSIS RESULTS".center(80))
        print("=" * 80 + "\n")
        print(summary)
        print("\n" + "=" * 80 + "\n")
        
        # Success message
        print("✅ Analysis complete!")
        print("\n")
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        sys.exit(1)


def analyze_batch_mode(directory: str, exclude_patterns: str = None, cache: bool = True):
    """Analyze all files in a project directory."""
    try:
        print_header()
        print(f"📁 Batch Analysis Mode")
        print(f"📂 Directory: {directory}")
        print("=" * 80 + "\n")
        
        # Parse exclude patterns
        exclude_set = None
        if exclude_patterns:
            exclude_set = set(p.strip() for p in exclude_patterns.split(','))
            print(f"🚫 Excluding: {', '.join(exclude_set)}\n")
        
        # Progress callback with tqdm
        pbar = None
        
        def progress_callback(current, total, filename):
            nonlocal pbar
            if pbar is None:
                pbar = tqdm(total=total, desc="Analyzing files", unit="file")
            pbar.update(1)
            pbar.set_postfix_str(f"Current: {filename[:40]}")
        
        # Analyze project
        results = analyze_project(
            directory,
            exclude_patterns=exclude_set,
            max_workers=4,
            progress_callback=progress_callback
        )
        
        if pbar:
            pbar.close()
        
        # Print summary
        summary = get_project_summary(results)
        print(summary)
        
        # Save cache if requested
        if cache and results['status'] == 'success':
            cache_dir = Path(directory) / '.cartographer_cache'
            cache_file = cache_dir / 'analysis.json'
            save_analysis_cache(results, str(cache_file))
        
        # Show file breakdown
        print("\n📊 Top Files by Function Count:")
        successful_files = [
            f for f in results['files'] 
            if f['status'] == 'success'
        ]
        sorted_files = sorted(
            successful_files,
            key=lambda x: len(x['analysis']['definitions']),
            reverse=True
        )[:10]
        
        for i, file_info in enumerate(sorted_files, 1):
            func_count = len(file_info['analysis']['definitions'])
            rel_path = os.path.relpath(file_info['file_path'], directory)
            print(f"  {i:2d}. {rel_path:50s} ({func_count} functions)")
        
        print("\n✅ Batch analysis complete!")
        print(f"💾 Results saved to: {cache_file if cache else 'not cached'}\n")
        
    except Exception as e:
        print(f"\n❌ Error during batch analysis: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        sys.exit(1)


def visualize_mode(directory: str, output: str = None, format: str = 'html', 
                   exclude_patterns: str = None, architecture: bool = False):
    """Generate dependency graph visualizations."""
    try:
        print_header()
        print(f"📊 Visualization Mode")
        print(f"📂 Directory: {directory}")
        print("=" * 80 + "\n")
        
        # Parse exclude patterns
        exclude_set = None
        if exclude_patterns:
            exclude_set = set(p.strip() for p in exclude_patterns.split(','))
        
        # Step 1: Batch analyze
        print("🔍 Step 1/3: Analyzing project files...")
        batch_results = analyze_project(directory, exclude_patterns=exclude_set, max_workers=4)
        
        if batch_results['status'] != 'success':
            print("❌ Failed to analyze project")
            return
        
        print(f"   ✓ Analyzed {batch_results['statistics']['successful']} files\n")
        
        # Step 2: Build dependency graph
        print("🔗 Step 2/3: Building dependency graph...")
        dep_analysis = analyze_dependencies(batch_results, directory)
        dep_summary = get_dependency_summary(dep_analysis, directory)
        print(dep_summary)
        
        # Step 3: Generate visualizations
        print("📊 Step 3/3: Generating visualizations...")
        
        # Determine output path
        if not output:
            output = f"dependency_graph.{format}"
        
        output_path = Path(output)
        
        # Generate graph
        fig = generate_dependency_graph(dep_analysis, directory)
        
        # Export based on format
        if format == 'html':
            export_graph_html(fig, str(output_path))
        elif format == 'png':
            export_graph_image(fig, str(output_path), format='png')
        elif format == 'svg':
            export_graph_image(fig, str(output_path), format='svg')
        elif format == 'json':
            export_graph_json(dep_analysis, str(output_path))
        
        # Generate statistics dashboard
        stats_output = output_path.parent / f"{output_path.stem}_stats.html"
        stats_fig = create_statistics_visualization(dep_analysis, batch_results, directory)
        export_graph_html(stats_fig, str(stats_output))
        
        # AI Architecture Analysis (if requested)
        if architecture:
            print("\n🤖 Generating AI architecture analysis...")
            print("   (This may take 30-60 seconds...)\n")
            
            arch_analysis = analyze_project_architecture(dep_analysis, batch_results, directory)
            
            print("=" * 80)
            print("ARCHITECTURE ANALYSIS".center(80))
            print("=" * 80 + "\n")
            print(arch_analysis)
            print("\n" + "=" * 80 + "\n")
            
            # Save to file
            arch_file = output_path.parent / f"{output_path.stem}_architecture.txt"
            with open(arch_file, 'w', encoding='utf-8') as f:
                f.write(arch_analysis)
            print(f"💾 Architecture analysis saved to: {arch_file}")
        
        print("\n✅ Visualization complete!")
        print(f"📊 View your graph: {output_path}")
        print(f"📈 View statistics: {stats_output}\n")
        
    except Exception as e:
        print(f"\n❌ Error during visualization: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point for the Code Cartographer CLI."""
    
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Code Cartographer - AI-powered code analysis tool',
        epilog='Examples:\n'
               '  Single file: python main.py services/parser.py\n'
               '  Batch mode:  python main.py --batch .\n'
               '  With exclude: python main.py --batch . --exclude "tests,docs"',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        help='Path to file or directory to analyze'
    )
    
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Batch mode: analyze all files in directory'
    )
    
    parser.add_argument(
        '--exclude',
        type=str,
        help='Comma-separated list of patterns to exclude (e.g., "tests,docs")'
    )
    
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Disable caching of analysis results'
    )
    
    parser.add_argument(
        '--visualize',
        action='store_true',
        help='Generate dependency graph visualization'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path for visualization (default: dependency_graph.html)'
    )
    
    parser.add_argument(
        '--format',
        type=str,
        choices=['html', 'png', 'svg', 'json'],
        default='html',
        help='Output format for visualization (default: html)'
    )
    
    parser.add_argument(
        '--architecture',
        action='store_true',
        help='Include AI-powered architecture analysis'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate arguments
    if not args.path:
        parser.print_help()
        sys.exit(1)
    
    # Check if path exists
    if not os.path.exists(args.path):
        print(f"❌ Error: Path not found: {args.path}")
        sys.exit(1)
    
    # Visualize mode
    if args.visualize:
        if not os.path.isdir(args.path):
            print(f"❌ Error: Visualization requires a directory, got: {args.path}")
            sys.exit(1)
        
        visualize_mode(
            args.path,
            output=args.output,
            format=args.format,
            exclude_patterns=args.exclude,
            architecture=args.architecture
        )
    
    # Batch mode
    elif args.batch:
        if not os.path.isdir(args.path):
            print(f"❌ Error: Batch mode requires a directory, got: {args.path}")
            sys.exit(1)
        
        analyze_batch_mode(
            args.path,
            exclude_patterns=args.exclude,
            cache=not args.no_cache
        )
    
    # Single file mode
    else:
        if not os.path.isfile(args.path):
            print(f"❌ Error: Not a file: {args.path}")
            print("💡 Tip: Use --batch flag to analyze entire directories")
            print("💡 Tip: Use --visualize flag to generate dependency graphs")
            sys.exit(1)
        
        analyze_single_file_mode(args.path)


if __name__ == "__main__":
    main()

