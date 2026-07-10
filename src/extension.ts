// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "cotran" is now active!');



	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	const disposable = vscode.commands.registerCommand('cotran.helloWorld', async () => {
		// The code you place here will be executed every time your command is executed
		// Display a message box to the user
		
	const repoPath = vscode.workspace.workspaceFolders?.[0].uri.fsPath;
	vscode.window.showInformationMessage('CoTran is loading...');

	const response = await fetch('http://127.0.0.1:8765/orient', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({repo_path: repoPath})
	});
	const data = await response.json() as {intro: {text: string}, waypoints: any[]};
	console.log(data)
	console.log(JSON.stringify(data));

	const introText = data.intro.text;
	const waypoints = data.waypoints;
	
	const panel = vscode.window.createWebviewPanel('CoTranIntro', 'CoTran', vscode.ViewColumn.One,{} );
	panel.webview.html = `
    	<!DOCTYPE html>
		<html>
    	<body>
        	<p>${introText}</p>
        	<button onclick="navigate()">Start Tour</button>
        	<script>
            	const vscode = acquireVsCodeApi();
            	function navigate() {
                	vscode.postMessage({ command: 'next', index: 0 });
            	}
        	</script>
    	</body>
    	</html>
	`;
	panel.webview.onDidReceiveMessage(async (message) => {
		if (message.command === 'next') {
			const waypoint = waypoints[message.index];
			const doc = await vscode.workspace.openTextDocument(waypoint.filepath);
			await vscode.window.showTextDocument(doc);
		}
	});

	

	});
	

	context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}
