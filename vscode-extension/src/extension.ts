import * as vscode from 'vscode';
import * as path from 'path';
import { spawn } from 'child_process';

export function activate(context: vscode.ExtensionContext) {
    console.log('Code Cartographer is now active!');

    // Get the workspace root and Python path
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0].uri.fsPath || '';
    const pythonPath = path.join(workspaceRoot, 'venv', 'bin', 'python');
    const mainScript = path.join(workspaceRoot, 'main.py');
    const dashboardScript = path.join(workspaceRoot, 'dashboard', 'app.py');

    // Command 1: Analyze Current File
    let analyzeFileCommand = vscode.commands.registerCommand('code-cartographer.analyzeFile', async () => {
        const editor = vscode.window.activeTextEditor;
        
        if (!editor) {
            vscode.window.showErrorMessage('No active file to analyze');
            return;
        }

        const filePath = editor.document.uri.fsPath;
        
        vscode.window.showInformationMessage(`Analyzing: ${path.basename(filePath)}...`);

        try {
            const result = await runPythonScript(pythonPath, mainScript, [filePath]);
            
            // Show results in a new document
            const doc = await vscode.workspace.openTextDocument({
                content: result,
                language: 'markdown'
            });
            await vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
            
            vscode.window.showInformationMessage('✅ Analysis complete!');
        } catch (error) {
            vscode.window.showErrorMessage(`Analysis failed: ${error}`);
        }
    });

    // Command 2: Analyze Entire Workspace
    let analyzeWorkspaceCommand = vscode.commands.registerCommand('code-cartographer.analyzeWorkspace', async (uri?: vscode.Uri) => {
        const targetPath = uri?.fsPath || workspaceRoot;
        
        if (!targetPath) {
            vscode.window.showErrorMessage('No workspace folder found');
            return;
        }

        const result = await vscode.window.showQuickPick(
            ['Yes, analyze entire workspace', 'No, cancel'],
            {
                placeHolder: `This will analyze all files in: ${path.basename(targetPath)}`
            }
        );

        if (result !== 'Yes, analyze entire workspace') {
            return;
        }

        vscode.window.showInformationMessage(`🔍 Analyzing workspace: ${path.basename(targetPath)}...`);

        try {
            await vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: "Code Cartographer",
                cancellable: false
            }, async (progress) => {
                progress.report({ message: "Analyzing project files..." });
                
                const result = await runPythonScript(pythonPath, mainScript, [
                    '--batch',
                    targetPath,
                    '--exclude',
                    'node_modules,venv,__pycache__,.git,dist,build'
                ]);
                
                // Show results
                const doc = await vscode.workspace.openTextDocument({
                    content: result,
                    language: 'markdown'
                });
                await vscode.window.showTextDocument(doc);
                
                return result;
            });
            
            vscode.window.showInformationMessage('✅ Workspace analysis complete!');
        } catch (error) {
            vscode.window.showErrorMessage(`Workspace analysis failed: ${error}`);
        }
    });

    // Command 3: Visualize Dependencies
    let visualizeCommand = vscode.commands.registerCommand('code-cartographer.visualizeWorkspace', async () => {
        const targetPath = workspaceRoot;
        
        if (!targetPath) {
            vscode.window.showErrorMessage('No workspace folder found');
            return;
        }

        vscode.window.showInformationMessage(`📊 Generating dependency visualization...`);

        try {
            await vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: "Code Cartographer",
                cancellable: false
            }, async (progress) => {
                progress.report({ message: "Building dependency graph..." });
                
                const outputPath = path.join(targetPath, 'cartographer_graph.html');
                
                await runPythonScript(pythonPath, mainScript, [
                    '--visualize',
                    targetPath,
                    '--architecture',
                    '--output',
                    outputPath
                ]);
                
                // Open the HTML file in browser
                const uri = vscode.Uri.file(outputPath);
                await vscode.env.openExternal(uri);
                
                return outputPath;
            });
            
            vscode.window.showInformationMessage('✅ Visualization generated! Opening in browser...');
        } catch (error) {
            vscode.window.showErrorMessage(`Visualization failed: ${error}`);
        }
    });

    // Command 4: Open Dashboard
    let openDashboardCommand = vscode.commands.registerCommand('code-cartographer.openDashboard', async () => {
        vscode.window.showInformationMessage('🚀 Starting Code Cartographer Dashboard...');

        try {
            // Start Flask server in background
            const dashboardProcess = spawn(pythonPath, [dashboardScript], {
                cwd: workspaceRoot,
                detached: true,
                stdio: 'ignore'
            });

            dashboardProcess.unref();

            // Wait a bit for server to start
            await new Promise(resolve => setTimeout(resolve, 2000));

            // Open browser
            await vscode.env.openExternal(vscode.Uri.parse('http://localhost:5000'));
            
            vscode.window.showInformationMessage('✅ Dashboard opened at http://localhost:5000');
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to start dashboard: ${error}`);
        }
    });

    context.subscriptions.push(
        analyzeFileCommand,
        analyzeWorkspaceCommand,
        visualizeCommand,
        openDashboardCommand
    );
}

// Helper function to run Python scripts
function runPythonScript(pythonPath: string, scriptPath: string, args: string[]): Promise<string> {
    return new Promise((resolve, reject) => {
        const process = spawn(pythonPath, [scriptPath, ...args]);
        
        let stdout = '';
        let stderr = '';
        
        process.stdout.on('data', (data) => {
            stdout += data.toString();
        });
        
        process.stderr.on('data', (data) => {
            stderr += data.toString();
        });
        
        process.on('close', (code) => {
            if (code === 0) {
                resolve(stdout);
            } else {
                reject(stderr || `Process exited with code ${code}`);
            }
        });
        
        process.on('error', (error) => {
            reject(error.message);
        });
    });
}

export function deactivate() {
    console.log('Code Cartographer deactivated');
}
