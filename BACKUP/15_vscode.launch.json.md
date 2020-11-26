# [vscode launch.json](https://github.com/chaleaoch/gitblog/issues/15)


Table of Contents
=================

   * [Variables Reference](#variables-reference)
      * [Predefined variables](#predefined-variables)
         * [Predefined variables examples](#predefined-variables-examples)
         * [Variables scoped per workspace folder](#variables-scoped-per-workspace-folder)
      * [Environment variables](#environment-variables)
      * [Configuration variables](#configuration-variables)
      * [Command variables](#command-variables)
      * [Input variables](#input-variables)
      * [Common questions](#common-questions)
         * [Details of variable substitution in a debug configuration or task](#details-of-variable-substitution-in-a-debug-configuration-or-task)
         * [Is variable substitution supported in User and Workspace settings?](#is-variable-substitution-supported-in-user-and-workspace-settings)
         * [Why isn't ${workspaceRoot} documented?](#why-isnt-workspaceroot-documented)
         * [How can I know a variable's actual value?](#how-can-i-know-a-variables-actual-value)

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
# Variables Reference

Visual Studio Code supports variable substitution in [Debugging](/docs/editor/debugging.md) and [Task](/docs/editor/tasks.md) configuration files as well as some select settings. Variable substitution is supported inside key and value strings in `launch.json` and `tasks.json` files using **${variableName}** syntax.

## Predefined variables

The following predefined variables are supported:

- **${workspaceFolder}** - the path of the folder opened in VS Code
- **${workspaceFolderBasename}** - the name of the folder opened in VS Code without any slashes (/)
- **${file}** - the current opened file
- **${relativeFile}** - the current opened file relative to `workspaceFolder`
- **${relativeFileDirname}** - the current opened file's dirname relative to `workspaceFolder`
- **${fileBasename}** - the current opened file's basename
- **${fileBasenameNoExtension}** - the current opened file's basename with no file extension
- **${fileDirname}** - the current opened file's dirname
- **${fileExtname}** - the current opened file's extension
- **${cwd}** - the task runner's current working directory on startup
- **${lineNumber}** - the current selected line number in the active file
- **${selectedText}** - the current selected text in the active file
- **${execPath}** - the path to the running VS Code executable
- **${defaultBuildTask}** - the name of the default build task

### Predefined variables examples

Supposing that you have the following requirements:

1. A file located at `/home/your-username/your-project/folder/file.ext` opened in your editor;
2. The directory `/home/your-username/your-project` opened as your root workspace.

So you will have the following values for each variable:

- **${workspaceFolder}** - `/home/your-username/your-project`
- **${workspaceFolderBasename}** - `your-project`
- **${file}** - `/home/your-username/your-project/folder/file.ext`
- **${relativeFile}** - `folder/file.ext`
- **${relativeFileDirname}** - `folder`
- **${fileBasename}** - `file.ext`
- **${fileBasenameNoExtension}** - `file`
- **${fileDirname}** - `/home/your-username/your-project/folder`
- **${fileExtname}** - `.ext`
- **${lineNumber}** - line number of the cursor
- **${selectedText}** - text selected in your code editor
- **${execPath}** - location of Code.exe

>**Tip**: Use IntelliSense inside string values for `tasks.json` and `launch.json` to get a full list of predefined variables.

### Variables scoped per workspace folder

By appending the root folder's name to a variable (separated by a colon), it is possible to reach into sibling root folders of a workspace. Without the root folder name, the variable is scoped to the same folder where it is used.

For example, in a multi root workspace with folders `Server` and `Client`, a `${workspaceFolder:Client}` refers to the path of the `Client` root.

## Environment variables

You can also reference environment variables through the **${env:Name}** syntax (for example, `${env:USERNAME}`).

```json
{
    "type": "node",
    "request": "launch",
    "name": "Launch Program",
    "program": "${workspaceFolder}/app.js",
    "cwd": "${workspaceFolder}",
    "args": [ "${env:USERNAME}" ]
}
```

## Configuration variables

You can reference VS Code settings ("configurations") through **${config:Name}** syntax (for example, `${config:editor.fontSize}`).

## Command variables

If the predefined variables from above are not sufficient, you can use any VS Code command as a variable through the **${command:commandID}** syntax.

A command variable is replaced with the (string) result from the command evaluation. The implementation of a command can range from a simple calculation with no UI, to some sophisticated functionality based on the UI features available via VS Code's extension API. If the command returns anything other than a string, then the variable replacement will not complete. Command variables **must** return a string.

An example of this functionality is in VS Code's Node.js debugger extension, which provides an interactive command `extension.pickNodeProcess` for selecting a single process from the list of all running Node.js processes. The command returns the process ID of the selected process. This makes it possible to use the `extension.pickNodeProcess` command in an **Attach by Process ID** launch configuration in the following way:

```json
{
    "configurations": [
        {
            "type": "node",
            "request": "attach",
            "name": "Attach by Process ID",
            "processId": "${command:extension.pickNodeProcess}"
        }
    ]
}
```

## Input variables

Command variables are already powerful but they lack a mechanism to configure the command being run for a specific use case. For example, it is not possible to pass a **prompt message** or a **default value** to a generic "user input prompt".

This limitation is solved with **input variables** which have the syntax: `${input:variableID}`. The `variableID` refers to entries in the `inputs` section of `launch.json` and `tasks.json`, where additional configuration attributes are specified.

The following example shows the overall structure of a `task.json` that makes use of input variables:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "task name",
            "command": "${input:variableID}",
            // ...
        }
    ],
    "inputs": [
        {
            "id": "variableID",
            "type": "type of input variable",
            // type specific configuration attributes
        }
    ]
}
```

Currently VS Code supports three types of input variables:

- **promptString**: Shows an input box to get a string from the user.
- **pickString**: Shows a Quick Pick dropdown to let the user select from several options.
- **command**: Runs an arbitrary command.

Each type requires additional configuration attributes:

`promptString`:

- **description**: Shown in the quick input, provides context for the input.
- **default**: Default value that will be used if the user doesn't enter something else.
- **password**: Set to true to input with a password prompt that will not show the typed value.

`pickString`:

- **description**: Shown in the quick pick, provides context for the input.
- **options**:  An array of options for the user to pick from.
- **default**: Default value that will be used if the user doesn't enter something else. It must be one of the option values.

`command`:

- **command**: Command being run on variable interpolation.
- **args**: Optional option bag passed to the command's implementation.

Below is an example of a `tasks.json` that illustrates the use of `inputs` using Angular CLI:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "ng g",
            "type": "shell",
            "command": "ng",
            "args": [
                "g",
                "${input:componentType}",
                "${input:componentName}"
            ],
        }
    ],
    "inputs": [
        {
            "type": "pickString",
            "id": "componentType",
            "description": "What type of component do you want to create?",
            "options": ["component", "directive", "pipe", "service", "class", "guard", "interface", "enum", "enum"],
            "default": "component"
        },
        {
            "type": "promptString",
            "id": "componentName",
            "description": "Name your component.",
            "default": "my-new-component"
        }
    ]
}
```

Running the example:

![Inputs Example](images/tasks/run-input-example.gif)

The following example shows how to use a user input variable of type `command` in a debug configuration that lets the user pick a test case from a list of all test cases found in a specific folder. It is assumed that some extension provides an `extension.mochaSupport.testPicker` command that locates all test cases in a configurable location and shows a picker UI to pick one of them. The arguments for a command input are defined by the command itself.

```json
{
    "configurations": [
        {
            "type": "node",
            "request": "launch",
            "name": "Run specific test",
            "program": "${workspaceFolder}/${input:pickTest}"
        }
    ],
    "inputs": [
        {
            "id": "pickTest",
            "type": "command",
            "command": "extension.mochaSupport.testPicker",
            "args": {
                "testFolder": "/out/tests",
            }
        }
    ]
}
```

Command inputs can also be used with tasks. In this example, the built-in Terminate Task command is used. It can accept an argument to terminate all tasks.

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Terminate All Tasks",
            "command": "echo ${input:terminate}",
            "type": "shell",
            "problemMatcher": []
        }
    ],
     "inputs": [
        {
            "id": "terminate",
            "type": "command",
            "command": "workbench.action.tasks.terminate",
            "args": "terminateAll"
        }
    ]
}
```

## Common questions

### Details of variable substitution in a debug configuration or task

Variable substitution in debug configurations or tasks is a two pass process:

- In the first pass, all variables are evaluated to string results. If a variable occurs more than once, it is only evaluated once.
- In the second pass, all variables are substituted with the results from the first pass.

A consequence of this is that the evaluation of a variable (for example, a command-based variable implemented in an extension) has **no access** to other substituted variables in the debug configuration or task. It only sees the original variables. This means that variables cannot depend on each other (which ensures isolation and makes substitution robust against evaluation order).

### Is variable substitution supported in User and Workspace settings?

The predefined variables are supported in a select number of setting keys in `settings.json` files such as the terminal `cwd`, `env`, `shell` and `shellArgs` values. Some [settings](/docs/getstarted/settings.md) like `window.title` have their own variables:

```json
  "window.title": "${dirty}${activeEditorShort}${separator}${rootName}${separator}${appName}"
```

Refer to the comments in the Settings editor (`kb(workbench.action.openSettings)`) to learn about setting specific variables.

### Why isn't ${workspaceRoot} documented?

The variable `${workspaceRoot}` was deprecated in favor of `${workspaceFolder}` to better align with [Multi-root Workspace](/docs/editor/multi-root-workspaces.md) support.

### How can I know a variable's actual value?

One easy way to check a variable's runtime value is to create a VS Code [task](/docs/editor/tasks.md) to output the variable value to the console. For example, to see the resolved value for `${workspaceFolder}`, you can create and run (**Terminal** > **Run Task**) the following simple 'echo' task in `tasks.json`:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "echo",
            "type": "shell",
            "command": "echo ${workspaceFolder}"
        }
    ]
}

---

Go
# Debugging

This document explains how to debug your Go programs in VS Code. The Go debugger is [Delve]. You can read more about it in the [Delve documentation](https://github.com/go-delve/delve/tree/master/Documentation).

## Overview

* [Set up](#set-up)
  * [Installation](#installation)
  * [Configuration](#configuration)
* [Launch Configurations](#launch-configurations)
  * [Specifying build tags](#specifying-build-tags)
  * [Using VS Code Variables](#using-vs-code-variables)
  * [Snippets](#snippets)
* [Debugging on Windows Subsystem for Linux (WSL)](#debugging-on-windows-subsystem-for-linux-wsl)
* [Remote Debugging](#remote-debugging)
* [Troubleshooting](#troubleshooting)
  * [Read documentation and common issues](#read-documentation-and-common-issues)
  * [Update Delve](#update-delve)
  * [Check for multiple versions of Delve](#check-for-multiple-versions-of-delve)
  * [Check your launch configuration](#check-your-launch-configuration)
  * [Check your GOPATH](#check-your-gopath)
  * [Enable logging](#enable-logging)
  * [Optional: Debug the debugger](#optional-debug-the-debugger)
  * [Ask for help](#ask-for-help)
* [Common issues](#common-issues)

## Set up

[Delve] should be installed by default when you install this extension.

You may need to update `dlv` to the latest version to support the latest version
of Go&mdash;see [Installation](#installation) below.

### Installation

You can also install Delve manually in one of two ways:

1. Open the [Command Palette][] (Windows/Linux: Ctrl+Shift+P; OSX: Shift+Command+P), select [`Go: Install/Update Tools`](settings.md#go-installupdate-tools), and select [`dlv`](tools.md#dlv).
2. Follow the [Delve installation instructions](https://github.com/go-delve/delve/tree/master/Documentation/installation).

### Start debugging

1. Open the `package main` source file or the test file you want to debug.
2. Start debugging using one of the following options:
   * Open the [Command Palette][], select
     `Debug: Start Debugging`, then select `Go`.
   * Open the debug window (Windows/Linux: Ctrl+Shift+D; OSX: Shift+Command+D) and click
     `Run and Debug`, then select `Go`.
   * Select **Run > Start Debugging** from the main menu.

   See [the VS Code Debugging documentation](https://code.visualstudio.com/docs/editor/debugging)
   for more information.

### Configuration

You may not need to configure any settings to start debugging your programs, but you should be aware that the debugger looks at the following settings.

* Related to [`GOPATH`](gopath.md):
  * [`go.gopath`](settings.md#go.gopath)
  * [`go.inferGopath`](settings.md#go.inferGopath)
* [`go.delveConfig`](settings.md#go.delveConfig)
  * `apiVersion`: Controls the version of the Delve API used (default: `2`).
  * `dlvLoadConfig`: The configuration passed to Delve, which controls how variables are shown in the Debug pane. Not applicable when `apiVersion` is 1.
    * `maxStringLen`: Maximum number of bytes read from a string (default: `64`).
    * `maxArrayValues`: Maximum number of elements read from an array, slice, or map (default: `64`).
    * `maxStructFields`: Maximum number of fields read from a struct. A setting of `-1` indicates that all fields should be read (default: `-1`).
    * `maxVariableRecurse`: How far to recurse when evaluating nested types (default: `1`).
    * `followPointers`: Automatically dereference pointers (default: `true`).
  * `showGlobalVariables`: Show global variables in the Debug view (default: `false`).

There are some common cases when you might want to tweak the Delve configurations.

* To change the default cap of 64 on string and array length when inspecting variables in the Debug view, set `maxStringLen`. (See a related known issue: [golang/vscode-go#126](https://github.com/golang/vscode-go/issues/126)).
* To evaluate nested variables in the Run view, set `maxVariableRecurse`.

## Launch Configurations

To get started debugging, run the command `Debug: Open launch.json`. If you did not already have a `launch.json` file for your project, this will create one for you. It will contain this default configuration, which can be used to debug the current package.

```json5
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Launch",
            "type": "go",
            "request": "launch",
            "mode": "auto",
            "program": "${fileDirname}",
            "env": {},
            "args": []
        }
    ]
}
```

There are some more properties that you can adjust in the debug configuration:

Property   | Description
--------   | -----------
name       | The name for your configuration as it appears in the drop-down in the Run view.
type       | Always leave this set to `"go"`. VS Code uses this setting to determine which extension should be used for debugging.
request    | One of `launch` or `attach`. Use `attach` when you want to attach to a running process.
mode       | For `launch` requests, one of `auto`, `debug`, `remote`, `test`, or `exec`. For `attach` requests, use `local` or `remote`.
program    | In `test` or `debug` mode, this refers to the absolute path to the package or file to debug. In `exec` mode, this is the existing binary file to debug. Not applicable to `attach` requests.
env        | Environment variables to use when debugging. Use the format: `{ "NAME": "VALUE" }`. Not applicable to `attach` requests.
envFile    | Absolute path to a file containing environment variable definitions. The environment variables passed in via the `env` property override the ones in this file.
args       | Array of command-line arguments to pass to the program being debugged.
showLog    | If `true`, Delve logs will be printed in the Debug Console panel.
logOutput  | Comma-separated list of Delve components (`debugger`, `gdbwire`, `lldbout`, `debuglineerr`, `rpc`) that should produce debug output when `showLog` is `true`.
buildFlags | Build flags to pass to the Go compiler.
remotePath | If remote debugging (`mode`: `remote`), this should be the absolute path to the package being debugged on the remote machine. See the section on [Remote Debugging](#remote-debugging) for further details. [golang/vscode-go#45](https://github.com/golang/vscode-go/issues/45) is also relevant.
cwd | The working directory to be used in running the program. If remote debugging (`mode`: `remote`), this should be the absolute path to the working directory being debugged on the local machine. See the section on [Remote Debugging](#remote-debugging) for further details. [golang/vscode-go#45](https://github.com/golang/vscode-go/issues/45) is also relevant.
processId  | This is the process ID of the executable you want to debug. Applicable only when using the `attach` request in `local` mode.

### Specifying [build tags](https://golang.org/pkg/go/build/#hdr-Build_Constraints)

If your program contains [build tags](https://golang.org/pkg/go/build/#hdr-Build_Constraints), you can use the `buildFlags` property. For example, if you build your code with:

```bash
go build -tags=whatever
```

Then, set:

```json5
"buildFlags": "-tags=whatever"
```

in your launch configuration. This property supports multiple tags, which you can set by using single quotes. For example:

```json5
"buildFlags": "-tags='first,second,third'"
```

<!--TODO(rstambler): Confirm that the extension works with a comma (not space) separated list.-->

### Using [VS Code variables]

Any property in the launch configuration that requires a file path can be specified in terms of [VS Code variables]. Here are some useful ones to know:

* `${workspaceFolder}` refers to the root of the workspace opened in VS Code.
* `${file}` refers to the currently opened file.
* `${fileDirname}` refers to the directory containing the currently opened file. This is typically also the name of the Go package containing this file, and as such, can be used to debug the currently opened package.

### Snippets

In addition to [VS Code variables], you can make use of [snippets] when editing the launch configuration in `launch.json`.

When you type `go` in the `launch.json` file, you will see snippet suggestions for debugging the current file or package or a given test function.

Below are the available sample configurations:

#### Debug the current file (`Go: Launch file`)

Recall that `${file}` refers to the currently opened file (see [Using VS Code Variables](#using-vs-code-variables)).

```json5
{
    "name": "Launch file",
    "type": "go",
    "request": "launch",
    "mode": "auto",
    "program": "${file}"
}
```

#### Debug a single test function (`Go: Launch test function`)

Recall that `${workspaceFolder}` refers to the current workspace (see [Using VS Code Variables](#using-vs-code-variables)). You will need to manually specify the function name instead of `"MyTestFunction"`.

```json5
{
    "name": "Launch test function",
    "type": "go",
    "request": "launch",
    "mode": "test",
    "program": "${workspaceFolder}",
    "args": [
        "-test.run",
        "MyTestFunction"
    ]
}
```

#### Debug all tests in the given package (`Go: Launch test package`)

Recall that `${workspaceFolder}` refers to the current workspace (see [Using VS Code Variables](#using-vs-code-variables)).

```json5
{
    "name": "Launch test package",
    "type": "go",
    "request": "launch",
    "mode": "test",
    "program": "${workspaceFolder}"
}
```

#### Attach to a running local process via its process ID (`Go: Attach to local process`)

Substitute the `0` below for the process ID (pid) of the process.

```json5
{
    "name": "Attach to local process",
    "type": "go",
    "request": "attach",
    "mode": "local",
    "processId": 0
}
```

#### Attach to a running server (`Go: Connect to Server`)

```json5
{
    "name": "Connect to server",
    "type": "go",
    "request": "attach",
    "mode": "remote",
    "remotePath": "${workspaceFolder}",
    "port": 2345,
    "host": "127.0.0.1"
}
```

#### Debug an existing binary

There is no snippet suggestion for this configuration.

```json
{
    "name": "Launch executable",
    "type": "go",
    "request": "launch",
    "mode": "exec",
    "program": "/absolute/path/to/executable"
}
```

If passing arguments to or calling subcommands and flags from a binary, the `args` property can be used.

```json
{
    "name": "Launch executable",
    "type": "go",
    "request": "launch",
    "mode": "exec",
    "program": "/absolute/path/to/executable",
    "args": ["subcommand", "arg", "--flag"],
}
```

## Debugging on [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/)

If you are using using WSL, you will need the WSL 2 Linux kernel.  See [WSL 2 Installation](https://docs.microsoft.com/en-us/windows/wsl/wsl2-install) and note the Window 10 build version requirements.

## Remote Debugging

<!--TODO(quoctruong): We use "remote" and "target", as well as "local" here. We should define these terms more clearly and be consistent about which we use.-->

To debug on a remote machine, you must first run a headless Delve server on the target machine. The examples below assume that you are in the same folder as the package you want to debug. If not, please refer to the [`dlv debug` documentation](https://github.com/go-delve/delve/blob/master/Documentation/usage/dlv_debug.md).

To start the headless Delve server:

```bash
dlv debug --headless --listen=:2345 --log --api-version=2
```

Any arguments that you want to pass to the program you are debugging must also be passed to this Delve server. For example:

```bash
dlv debug --headless --listen=:2345 --log -- -myArg=123
```

Then, create a remote debug configuration in your `launch.json`.

```json5
{
    "name": "Launch remote",
    "type": "go",
    "request": "attach",
    "mode": "remote",
    "remotePath": "/absolute/path/dir/on/remote/machine",
    "port": 2345,
    "host": "127.0.0.1",
    "cwd": "/absolute/path/dir/on/local/machine",
}
```

In the example, the VS Code debugger will run on the same machine as the headless `dlv` server. Make sure to update the `port` and `host` settings to point to your remote machine.

`remotePath` should point to the absolute path of the program being debugged in the remote machine. `cwd` should point to the absolute path of the working directory of the program being debugged on your local machine. This should be the counterpart of the folder in `remotePath`. See [golang/vscode-go#45](https://github.com/golang/vscode-go/issues/45) for updates regarding `remotePath` and `cwd`.

When you run the `Launch remote` target, VS Code will send debugging commands to the `dlv` server you started, instead of launching it's own `dlv` instance against your program.

For further examples, see [this launch configuration for a process running in a Docker host](https://github.com/lukehoban/webapp-go/tree/debugging).

## Troubleshooting

Debugging is one of the most complex features offered by this extension. The features are not complete, and a new implementation is currently being developed (see [golang/vscode-go#23](https://github.com/golang/vscode-go/issues/23)).

The suggestions below are intended to help you troubleshoot any problems you encounter. If you are unable to resolve the issue, please take a look at the [current known debugging issues](https://github.com/golang/vscode-go/issues?q=is%3Aissue+is%3Aopen+label%3Adebug) or [file a new issue](https://github.com/golang/vscode-go/issues/new/choose).

### Read documentation and [common issues](#common-issues)

Start by taking a quick glance at the [common issues](#common-issues) described below. You can also check the [Delve FAQ](https://github.com/go-delve/delve/blob/master/Documentation/faq.md) in case the problem is mentioned there.

### Update Delve

If the problem persists, it's time to start troubleshooting. A good first step is to make sure that you are working with the latest version of Delve. You can do this by running the [`Go: Install/Update Tools`](settings.md#go-installupdate-tools) command and selecting [`dlv`](tools.md#dlv).

### Check your [launch configuration](#launch-configurations)

Next, confirm that your [launch configuration](#launch-configurations) is correct.

One common error is `could not launch process: stat ***/debug.test: no such file or directory`. You may see this while running in the `test` mode. This happens when the `program` attribute points to a folder with no test files, so ensure that the `program` attribute points to a directory containing the test files you wish to debug.

Also, check the version of the Delve API used in your [launch configuration](#launch-configurations). This is handled by the `–api-version` flag, `2` is the default. If you are debugging on a remote machine, this is particularly important, as the versions on the local and remote machines much match. You can change the API version by editing the [`launch.json` file](#launch-configurations).

### Check for multiple versions of Delve

You might have multiple different versions of [`dlv`](tools.md#dlv) installed, and VS Code Go could be using a wrong or old version. Run the [`Go: Locate Configured Go Tools`](settings.md#go-locate-configured-go-tools) command and see where VS Code Go has found `dlv` on your machine. You can try running `which dlv` to see which version of `dlv` you are using on the [command-line](https://github.com/go-delve/delve/tree/master/Documentation/cli).

To fix the issue, simply delete the version of `dlv` used by the Go extension. Note that the extension first searches for binaries in your `$GOPATH/bin` and then looks on your `$PATH`.

If you see the error message `Failed to continue: "Error: spawn EACCES"`, the issue is probably multiple versions of `dlv`.

### Try building your binary **without** compiler optimizations

If you notice `Unverified breakpoints` or missing variables, ensure that your binary was built **without** compiler optimizations. Try building the binary with `-gcflags="all=-N -l"`.

### Check your `GOPATH`

Make sure that the debugger is using the right [`GOPATH`](gopath.md). This is probably the issue if you see `Cannot find package ".." in any of ...` errors. Read more about configuring your [GOPATH](gopath.md) or [file an issue report](https://github.com/golang/vscode-go/issues/new/choose).

**As a work-around**, add the correct `GOPATH` as an environment variable in the `env` property in the `launch.json` file.

### Enable logging

Next, check the logs produced by Delve. These will need to be manually enabled. Follow these steps:

* Set `"showLog": true` in your launch configuration. This will show Delve logs in the Debug Console pane (Ctrl+Shift+Y).
* Set `"trace": "log"` in your launch configuration. Again, you will see logs in the Debug Console pane (Ctrl+Shift+Y). These logs will also be saved to a file and the path to this file will be printed at the top of the Debug Console.
* Set `"logOutput": "rpc"` in your launch configuration. You will see logs of the RPC messages going between VS Code and Delve. Note that for this to work, you must also have set `"showLog": true`.
  * The `logOutput` attribute corresponds to the `--log-output` flag used by Delve. It is a comma-separated list of components that should produce debug output.

See [common issues](#common-issues) below to decipher error messages you may find in your logs.

With `"trace": "log"`, you will see the actual call being made to `dlv`. To aid in your investigation, you can copy that and run it in your terminal.

### **Optional**: Debug the debugger

This is not a required step, but if you want to continue digging deeper, you can, in fact, debug the debugger. The code for the debugger can be found in the [debug adapter module](../src/debugAdapter). See our [contribution guide](contributing.md) to learn how to [run](contributing.md#run) and [sideload](contributing.md#sideload) the Go extension.

### Ask for help

At this point, it's time to look at the [common issues](#common-issues) below or the [existing debugging issues](https://github.com/golang/vscode-go/issues?q=is%3Aissue+is%3Aopen+label%3Adebug) on the [issue tracker](https://github.com/golang/vscode-go/issues). If that still doesn't solve your problem, [file a new issue](https://github.com/golang/vscode-go/issues/new/choose) or ask a question on the `#vscode` channel of the [Gophers Slack](https://gophers.slack.com).

## Common Issues

### delve/launch hangs with no messages on WSL

Try running ```delve debug ./main``` in the WSL command line and see if you get a prompt.

**_Solution_**: Ensure you are running the WSL 2 Kernel, which (as of 4/15/2020) requires an early release of the Windows 10 OS. This is available to anyone via the Windows Insider program. See [Debugging on WSL](#debugging-on-windows-subsystem-for-linux-wsl).

### could not launch process: could not fork/exec

The solution this issue differs based on your OS.

#### OSX

This usually happens on OSX due to signing issues. See the discussions in [Microsoft/vscode-go#717](https://github.com/Microsoft/vscode-go/issues/717), [Microsoft/vscode-go#269](https://github.com/Microsoft/vscode-go/issues/269) and [go-delve/delve#357](https://github.com/go-delve/delve/issues/357).

**_Solution_**: You may have to uninstall dlv and install it manually as described in the [Delve instructions](https://github.com/go-delve/delve/blob/master/Documentation/installation/osx/install.md#manual-install).

#### Linux/Docker

Docker has security settings preventing `ptrace(2)` operations by default within the container.

**_Solution_**: To run your container insecurely, pass `--security-opt=seccomp:unconfined` to `docker run`. See [go-delve/delve#515](https://github.com/go-delve/delve/issues/515) for references.

#### could not launch process: exec: "lldb-server": executable file not found in $PATH

This error can show up for Mac users using Delve versions 0.12.2 and above. `xcode-select --install` has solved the problem for a number of users.

### Debugging symlink directories

This extension does not provide support for debugging projects containing symlinks. Make sure that you are setting breakpoints in the files that Go will use to compile your program.

For updates to symlink support reference [golang/vscode-go#622](https://github.com/golang/vscode-go/issues/622).

[Delve]: https://github.com/go-delve/delve
[VS Code variables]: https://code.visualstudio.com/docs/editor/variables-reference
[snippets]: https://code.visualstudio.com/docs/editor/userdefinedsnippets
[Command Palette]: https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette

---

# Python debug configurations in Visual Studio Code

The Python extension supports debugging of a number of types of Python applications. For a short walkthrough of basic debugging, see [Tutorial - Configure and run the debugger](/docs/python/python-tutorial.md#configure-and-run-the-debugger). Also see the [Flask tutorial](/docs/python/tutorial-flask.md). Both tutorials demonstrate core skills like setting breakpoints and stepping through code.

**For general debugging features** such as inspecting variables, setting breakpoints, and other activities that aren't language-dependent, review [VS Code debugging](/docs/editor/debugging.md).

This article addresses only those considerations that are specific to Python, mainly Python-specific debugging *configurations*, including the necessary steps for specific app types and remote debugging.

## Initialize configurations

A configuration drives VS Code's behavior during a debugging session. Configurations are defined in a `launch.json` file that's stored in a `.vscode` folder in your workspace.

> **Note** In order to change debugging configuration, your code must be stored in a folder.

To initialize debug configurations, first select the Run view in the sidebar:

![Run icon](images/debugging/debug-icon.png)

If you don't yet have any configurations defined, you'll see a button to Run and Debug, as well as a link to create a configuration (launch.json) file:

![Debug toolbar settings command](images/debugging/debug-start.png)

To generate a `launch.json` file with Python configurations, do the following steps:

1. Click the **create a launch.json file** link (circled in the image above) or use the **Run** > **Open configurations** menu command.

1. A configuration menu will open from the Command Palette allowing you to choose the type of debug configuration you want for the opened file. For now, in the **Select a debug configuration** menu that appears, select **Python File**.
![Debug configurations menu](images/debugging/debug-configurations.png)

   > **Note** Starting a debugging session through the Debug Panel, **F5** or **Run > Start Debugging**, when no configuration exists will also bring up the debug configuration menu, but will not create a launch.json file.

1. The Python extension then creates and opens a `launch.json` file that contains a pre-defined configuration based on what you previously selected, in this case **Python File**. You can modify configurations (to add arguments, for example), and also add custom configurations.

   ![Configuration json](images/debugging/configuration-json.png)

The details of configuration properties are covered later in this article under [Standard configuration and options](#set-configuration-options). Additional configurations are also described in this article under [Debugging specific app types](#debugging-specific-app-types).

## Additional configurations

By default, VS Code shows only the most common configurations provided by the Python extension. You can select other configurations to include in `launch.json` by using the **Add Configuration** command shown in the list and in the `launch.json` editor. When you use the command, VS Code prompts you with a list of all available configurations (be sure to scroll down to see  all the Python options):

![Adding a new Python debugging configuration](images/debugging/add-configuration.png)

Selecting the **Node.js: Gulp task** yields the following result:
![Added a configuration](images/debugging/added-configuration.png)

See [Debugging specific app types](#debugging-specific-app-types) for details on all of these configurations.

During debugging, the Status Bar shows the current configuration and the current debugging interpreter. Selecting the configuration brings up a list from which you can choose a different configuration:

![Debugging Status Bar](images/debugging/debug-status-bar.png)

By default, the debugger uses the same `python.pythonPath` workspace setting as for other features of VS Code. To use a different interpreter for debugging specifically, set the value for `python` in `launch.json` for the applicable debugger configuration. Alternately, select the named interpreter on the Status Bar to select a different one.

## Basic debugging

The simplest way to begin debugging a Python file is to use the **Run** view and click the **Run and Debug** button. When no configuration has been previously set, you will be presented with a list of debugging options. Select the appropriate option to quickly begin debugging your code.

![Run the debugger](images/debugging/debug-run.png)

Two common options are to use the **Python File** configuration to run the currently open Python file or to use the **Attach using Process ID** configuration to attach the debugger to a process that is already running.

For information about creating and using debugging configurations see the [Initialize configurations](#initialize-configurations) and [Additional configurations](#additional-configurations) sections. Once a configuration is added, it can be selected from the dropdown list and started using the **Start Debugging** button.

![Start debugging](images/debugging/debug-start-button.png)

## Command line debugging

The debugger can also be run from the command line. The debugger command line syntax is as follows:

```bash
python -m debugpy
    --listen | --connect
    [<host>:]<port>
    [--wait-for-client]
    [--configure-<name> <value>]...
    [--log-to <path>] [--log-to-stderr]
    <filename> | -m <module> | -c <code> | --pid <pid>
    [<arg>]...
```

As an example, from the command line, you could start the debugger using a specified port (5678) and script using the following syntax. This example assumes the script is long running and omits the `--wait-for-client` flag, meaning that the script will not wait for the client to attach.

```bash
python -m debugpy --listen 5678 ./myscript.py
```

You would then use the following configuration to attach from the VS Code Python extension.

```json
{
    "name": "Python: Attach",
    "type": "python",
    "request": "attach",
    "connect": {
        "host": "localhost",
        "port": 5678
    }
}
```

> **Note**: Specifying host is optional for **listen**, by default 127.0.0.1 is used.

If you wanted to debug remote code or code running in a docker container, on the remote machine or container, you would need to modify the previous CLI command to specify a host.

```bash
python -m debugpy --listen 0.0.0.0:5678 ./myscript.py
```

The associated configuration file would then look as follows.

```json
{
    "name": "Attach",
    "type": "python",
    "request": "attach",
    "host": "remote-machine-name", // replace this with remote machine name
    "port": 5678,
}
```

> **Note**: Be aware that when you specify a host value other than `127.0.0.1` or `localhost` you are opening a port to allow access from any machine, which carries security risks. You should make sure that you're taking appropriate security precautions, such as using SSH tunnels, when doing remote debugging.

|Flag  |Options  |Description  |
|---------|---------|---------|
|**--listen** or **--connect**  |  `[<host>:]<port>`       |   **Required**. Specifies the host address and port for the debug adapter server to wait for incoming connections (--listen) or to connect with a client that is waiting for an incoming connection (--connect). This is the same address that is used in the VS Code debug configuration. By default the host address is `localhost (127.0.0.1)`.      |
|**--wait-for-client**     |   none      | **Optional**. Specifies that the code should not run until there's a connection from the debug server. This setting allows you to debug from the first line of your code.        |
|**--log-to**     |   `<path>`      | **Optional**. Specifies a path to an existing directory for saving logs.         |
|**--log-to-stderr**     |    none     |  **Optional**. Enables debugpy to write logs directly to stderr.       |
|**--pid**     |    `<pid>`     | **Optional**. Specifies a process that is already running to inject the debug server into.        |
|**--configure-\<name>** | `<value>` | **Optional**. Sets a debug property that must be known to the debug server before the client connects. Such properties can be used directly in *launch* configuration, but must be set in this manner for *attach* configurations. For example, if you don't want the debug server to automatically inject itself into subprocesses created by the process you're attaching to, use `--configure-subProcess false`.|

> **Note**: `[<arg>]` can be used to pass command line arguments along to the app being launched.

## Debugging by attaching over a network connection

### Local script debugging

In some scenarios, you need to debug a Python script that's invoked locally by another process. For example, you may be debugging a web server that runs different Python scripts for specific processing jobs. In such cases, you need to attach the VS Code debugger to the script once it's been launched:

1. Run VS Code, open the folder or workspace containing the script, and create a `launch.json` for that workspace if one doesn't exist already.

1. In the script code, add the following and save the file:

    ```python
    import debugpy

    # 5678 is the default attach port in the VS Code debug configurations. Unless a host and port are specified, host defaults to 127.0.0.1
    debugpy.listen(5678)
    print("Waiting for debugger attach")
    debugpy.wait_for_client()
    debugpy.breakpoint()
    print('break on this line')
    ```

1. Open a terminal using **Terminal: Create New Integrated Terminal**, which activates the script's selected environment.

1. In the terminal, install the debugpy package with `python -m pip install --upgrade debugpy`.

1. In the terminal, start Python with the script, for example, `python3 myscript.py`. You should see the "Waiting for debugger attach" message that's included in the code, and the script halts at the `debugpy.wait_for_client()` call.

1. Switch to the Run view, select the appropriate configuration from the debugger drop-down list, and start the debugger.

1. The debugger should stop on the `debugpy.breakpoint()` call, from which point you can use the debugger normally. You can, of course, set other breakpoints in the script code using the UI instead of using `debugpy.breakpoint()`.

### Remote script debugging with SSH

Remote debugging allows you to step through a program locally within VS Code while it runs on a remote computer. It is not necessary to install VS Code on the remote computer. For added security, you may want or need to use a secure connection, such as SSH, to the remote computer when debugging.

> **Note**: On Windows computers, you may need to install [Windows 10 OpenSSH](https://docs.microsoft.com/windows-server/administration/openssh/openssh_install_firstuse) to have the `ssh` command.

The following steps outline the general process to set up an SSH tunnel. An SSH tunnel allows you to work on your local machine as if you were working directly on the remote in a more secure manner than if a port was opened for public access.

**On the remote computer:**

1. Enable port forwarding by opening the `sshd_config` config file (found under `/etc/ssh/` on Linux and under `%programfiles(x86)%/openssh/etc` on Windows) and adding or modifying the following setting:

    ```
    AllowTcpForwarding yes
    ```

   > **Note**: The default for AllowTcpForwarding is yes, so you might not need to make a change.

1. If you had to add or modify `AllowTcpForwarding`, restart the SSH server. On Linux/macOS, run `sudo service ssh restart`; on Windows, run `services.msc`, locate and select OpenSSH or `sshd` in the list of services, and select **Restart**.

**On the local computer:**

1. Create an SSH tunnel by running `ssh -2 -L sourceport:localhost:destinationport -i identityfile user@remoteaddress`, using a selected port for `destinationport` and the appropriate username and the remote computer's IP address in `user@remoteaddress`. For example, to use port 5678 on IP address 1.2.3.4, the command would be `ssh -2 -L 5678:localhost:5678 -i identityfile user@1.2.3.4`. You can specify the path to an identity file, using the `-i` flag.

1. Verify that you can see a prompt in the SSH session.

1. In your VS Code workspace, create a configuration for remote debugging in your `launch.json` file, setting the port to match the port used in the `ssh` command and the host to `localhost`. You use `localhost` here because you've set up the SSH tunnel.

    ```json
    {
        "name": "Python: Attach",
        "type": "python",
        "request": "attach",
        "port": 5678,
        "host": "localhost",
        "pathMappings": [
            {
                "localRoot": "${workspaceFolder}", // Maps C:\Users\user1\project1
                "remoteRoot": "."                  // To current working directory ~/project1
            }
        ]
    }
    ```

**Starting debugging**

Now that an SSH tunnel has been set up to the remote computer, you can begin your debugging.

1. Both computers: make sure that identical source code is available.

1. Both computers: install [debugpy](https://pypi.org/project/debugpy/) using `python -m pip install --upgrade debugpy` into your environment (while using a form of virtual environment is not required, it is a recommended best practice).

1. Remote computer: there are two ways to specify how to attach to the remote process.

   1. In the source code, add the following lines, replacing `address` with the remote computer's IP address and port number (IP address 1.2.3.4 is shown here for illustration only).

        ```python
        import debugpy

        # Allow other computers to attach to debugpy at this IP address and port.
        debugpy.listen(('1.2.3.4', 5678))

        # Pause the program until a remote debugger is attached
        debugpy.wait_for_client()
        ```

        The IP address used in `listen` should be the remote computer's private IP address. You can then launch the program normally, causing it to pause until the debugger attaches.

   1. Launch the remote process through debugpy, for example:

       ```bash
       python3 -m debugpy --listen 1.2.3.4:5678 --wait-for-client -m myproject
       ```

       This starts the package `myproject` using `python3`, with the remote computer's private IP address of `1.2.3.4` and listening on port `5678` (you can also start the remote Python process by specifying a file path instead of using `-m`, such as `./hello.py`).

1. Local computer: **Only if you modified the source code on the remote computer as outlined above**, then in the source code, add a commented-out copy of the same code added on the remote computer. Adding these lines makes sure that the source code on both computers matches line by line.

    ```python
    #import debugpy

    # Allow other computers to attach to debugpy at this IP address and port.
    #debugpy.listen(('1.2.3.4', 5678))

    # Pause the program until a remote debugger is attached
    #debugpy.wait_for_client()
    ```

1. Local computer: switch to the Run view in VS Code, select the **Python: Attach** configuration

1. Local computer: set a breakpoint in the code where you want to start debugging.

1. Local computer: start the VS Code debugger using the modified **Python: Attach** configuration and the Start Debugging button. VS Code should stop on your locally set breakpoints, allowing you to step through the code, examine variables, and perform all other debugging actions. Expressions that you enter in the **Debug Console** are run on the remote computer as well.

    Text output to stdout, as from `print` statements, appears on both computers. Other outputs, such as graphical plots from a package like matplotlib, however, appear only on the remote computer.

1. During remote debugging, the debugging toolbar appears as below:

    ![Debugging toolbar during remote debugging](images/debugging/remote-debug-toolbar.png)

    On this toolbar, the disconnect button (`kb(workbench.action.debug.stop)`) stops the debugger and allows the remote program to run to completion. The restart button (`kb(workbench.action.debug.restart)`) restarts the debugger on the local computer but does **not** restart the remote program. Use the restart button only when you've already restarted the remote program and need to reattach the debugger.

## Set configuration options

When you first create `launch.json`, there are two standard configurations that run the active file in the editor in either the integrated terminal (inside VS Code) or the external terminal (outside of VS Code):

```json
{
    "name": "Python: Current File (Integrated Terminal)",
    "type": "python",
    "request": "launch",
    "program": "${file}",
    "console": "integratedTerminal"
},
{
    "name": "Python: Current File (External Terminal)",
    "type": "python",
    "request": "launch",
    "program": "${file}",
    "console": "externalTerminal"
}
```

The specific settings are described in the following sections. You can also add other settings, such as `args`, that aren't included in the standard configurations.

> **Tip**: It's often helpful in a project to create a configuration that runs a specific startup file. For example, if you want to always launch `startup.py` with the arguments `--port 1593` when you start the debugger, create a configuration entry as follows:

```json
 {
     "name": "Python: startup.py",
     "type": "python",
     "request": "launch",
     "program": "${workspaceFolder}/startup.py",
     "args" : ["--port", "1593"]
 },
```

### `name`

Provides the name for the debug configuration that appears in the VS Code drop-down list.

### `type`

Identifies the type of debugger to use; leave this set to `python` for Python code.

### `request`

Specifies the mode in which to start debugging:

- `launch`: start the debugger on the file specified in `program`
- `attach`: attach the debugger to an already running process. See [Remote debugging](#remote-script-debugging-with-ssh) for an example.

### `program`

Provides the fully qualified path to the python program's entry module (startup file). The value `${file}`, often used in default configurations, uses the currently active file in the editor. By specifying a specific startup file, you can always be sure of launching your program with the same entry point regardless of which files are open. For example:

```json
"program": "/Users/Me/Projects/PokemonGo-Bot/pokemongo_bot/event_handlers/__init__.py",
```

You can also rely on a relative path from the workspace root. For example, if the root is `/Users/Me/Projects/PokemonGo-Bot` then you can use the following:

```json
"program": "${workspaceFolder}/pokemongo_bot/event_handlers/__init__.py",
```

### `python`

Full path that points to the Python interpreter to be used for debugging.

If not specified, this setting defaults to the interpreter identified in the `python.pythonPath` setting, which is equivalent to using the value `${config:python.pythonPath}`. To use a different interpreter, specify its path instead in the `python` property of a debug configuration.

Alternately, you can use a custom environment variable that's defined on each platform to contain the full path to the Python interpreter to use, so that no additional folder paths are needed.

If you need to pass arguments to the Python interpreter, you can use the syntax `"python": ["<path>", "<arg>",...]`.

### `args`

Specifies arguments to pass to the Python program. Each element of the argument string that's separated by a space should be contained within quotes, for example:

```json
"args": ["--quiet", "--norepeat", "--port", "1593"],
```

### `stopOnEntry`

When set to `true`, breaks the debugger at the first line of the program being debugged. If omitted (the default) or set to `false`, the debugger runs the program to the first breakpoint.

### `console`

Specifies how program output is displayed as long as the defaults for `redirectOutput` aren't modified.

| Value                            | Where output is displayed                                          |
|----------------------------------|--------------------------------------------------------------------|
| `"internalConsole"`              | **VS Code debug console.** If `redirectOutput` is set to False, no output is displayed.                                 |
| `"integratedTerminal"` (default) | [VS Code Integrated Terminal](/docs/editor/integrated-terminal.md). If `redirectOutput` is set to True, output is also displayed in the debug console.|
| `"externalTerminal"`             | **Separate console window**. If `redirectOutput` is set to True, output is also displayed in the debug console.                                            |

### `cwd`

Specifies the current working directory for the debugger, which is the base folder for any relative paths used in code. If omitted, defaults to `${workspaceFolder}` (the folder open in VS Code).

As an example, say `${workspaceFolder}` contains a `py_code` folder containing `app.py`, and a `data` folder containing `salaries.csv`. If you start the debugger on `py_code/app.py`, then the relative paths to the data file vary depending on the value of `cwd`:

| cwd | Relative path to data file |
| --- | --- |
| Omitted or `${workspaceFolder}` | `data/salaries.csv` |
| `${workspaceFolder}/py_code` | `../data/salaries.csv` |
| `${workspaceFolder}/data` | `salaries.csv` |

### `redirectOutput`

When omitted or set to `true` (the default for internalConsole), causes the debugger to print all output from the program into the VS Code debug output window. If set to `false` (the default for integratedTerminal and externalTerminal), program output is not displayed in the debugger output window.

This option is typically disabled when using `"console": "integratedTerminal"` or `"console": "externalTerminal"` because there's no need to duplicate the output in the debug console.

### `justMyCode`

When omitted or set to `true` (the default), restricts debugging to user-written code only. Set to `false` to also enable debugging of standard library functions.

### `django`

When set to `true`, activates debugging features specific to the Django web framework.

### `sudo`

When set to `true` and used with `"console": "externalTerminal"`, allows for debugging apps that require elevation. Using an external console is necessary to capture the password.

### `pyramid`

When set to `true`, ensures that a Pyramid app is launched with [the necessary `pserve` command](https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/startup.html?highlight=pserve).

### `env`

Sets optional environment variables for the debugger process beyond system environment variables, which the debugger always inherits. The values for these variables must be entered as strings.

### `envFile`

Optional path to a file that contains environment variable definitions. See [Configuring Python environments - environment variable definitions file](/docs/python/environments.md#environment-variable-definitions-file).

### `gevent`

If set to `true`, enables debugging of [gevent monkey-patched code](https://www.gevent.org/intro.html).

## Breakpoints and logpoints

The Python extension supports [breakpoints](/docs/editor/debugging.md#breakpoints) and [logpoints](/docs/editor/debugging.md#logpoints) for debugging code. For a short walkthrough of basic debugging and using breakpoints, see [Tutorial - Configure and run the debugger](/docs/python/python-tutorial.md#configure-and-run-the-debugger).

### Conditional breakpoints

Breakpoints can also be set to trigger based on expressions, hit counts, or a combination of both. The Python extension support hit counts that are integers, as well as integers preceded by the ==, >, >=, <, <=, and % operators. For example, you could set a breakpoint to trigger after 5 occurrences by setting a hitcount of `>5`  For more information, see [conditional breakpoints](/docs/editor/debugging.md#conditional-breakpoints) in the main VS Code debugging article.

### Invoking a breakpoint in code

In your Python code, you can call `debugpy.breakpoint()` at any point where you want to pause the debugger during a debugging session.

### Breakpoint validation

The Python extension automatically detects breakpoints that are set on non-executable lines, such as `pass` statements or the middle of a multiline statement. In such cases, running the debugger moves the breakpoint to nearest valid line to ensure that code execution stops at that point.

## Debugging specific app types

The configuration drop-down provides a variety of different options for general app types:

| Configuration | Description |
| --- | --- |
| Attach | See [Remote debugging](#remote-debugging) in the previous section. |
| Django | Specifies `"program": "${workspaceFolder}/manage.py"`, `"args": ["runserver", "--noreload"]`, and `"console": "integratedTerminal"`. Also adds `"django": true` to enable debugging of Django HTML templates. Note that automatic reloading of Django apps is not possible while debugging. |
| Flask | See [Flask debugging](#flask-debugging) below. |
| Gevent | Adds `"gevent": true` to the standard integrated terminal configuration. |
| Pyramid | Removes `program`, adds `"args": ["${workspaceFolder}/development.ini"]`, adds `"jinja": true` for enabling template debugging, and adds `"pyramid": true` to ensure that the program is launched with [the necessary `pserve` command](https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/startup.html?highlight=pserve). |
| Scrapy | Specifies `"module": "scrapy"`  and adds `"args": ["crawl", "specs", "-o", "bikes.json"]`. |
| Watson | Specifies `"program": "${workspaceFolder}/console.py"` and `"args": ["dev", "runserver", "--noreload=True"]`. |

Specific steps are also needed for remote debugging and Google App Engine. For details on debugging tests (including nosetest), see [Testing](/docs/python/testing.md).

To debug an app that requires administrator privileges, use `"console": "externalTerminal"` and `"sudo": "True"`.

### Flask debugging

```json
{
    "name": "Python: Flask",
    "type": "python",
    "request": "launch",
    "module": "flask",
    "env": {
        "FLASK_APP": "app.py"
    },
    "args": [
        "run",
        "--no-debugger",
        "--no-reload"
    ],
    "jinja": true
},
```

As you can see, this configuration specifies `"env": {"FLASK_APP": "app.py"}` and `"args": ["run", "--no-debugger","--no-reload"]`. The `"module": "flask"` property is used instead of `program`. (You may see `"FLASK_APP": "${workspaceFolder}/app.py"` in the `env` property, in which case modify the configuration to refer to only the filename. Otherwise you may see "Cannot import module C" errors where C is a drive letter.)

The `"jinja": true` setting also enables debugging for Flask's default Jinja templating engine.

If you want to run Flask's development server in development mode, use the following configuration:

```json
{
    "name": "Python: Flask (development mode)",
    "type": "python",
    "request": "launch",
    "module": "flask",
    "env": {
        "FLASK_APP": "app.py",
        "FLASK_ENV": "development"
    },
    "args": [
        "run"
    ],
    "jinja": true
},
```

<a name="debugger-not-working"></a>

## Troubleshooting

There are many reasons why the debugger may not work. Oftentimes the debug console reveals specific causes, but two specific reasons are as follows:

- The path to the python executable is incorrect: check the value of `python.pythonPath` in your user settings.
- There are invalid expressions in the watch window: clear all expressions from the Watch window and restart the debugger.
- If you're working with a multi-threaded app that uses native thread APIs (such as the Win32 `CreateThread` function rather than the Python threading APIs), it's presently necessary to include the following source code at the top of whichever file you wish to debug:

    ```python
    import debugpy
    debugpy.debug_this_thread()
    ```

## Next steps

- [Python environments](/docs/python/environments.md) - Control which Python interpreter is used for editing and debugging.
- [Testing](/docs/python/testing.md) - Configure test environments and discover, run, and debug tests.
- [Settings reference](/docs/python/settings-reference.md) - Explore the full range of Python-related settings in VS Code.
- [General debugging](/docs/editor/debugging.md) - Learn about the debugging features of VS Code.
