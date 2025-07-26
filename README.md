# CirChecker

A static analysis tool for Circom source code, designed to detect security vulnerabilities in Zero-Knowledge Proof (ZKP) circuits written in the Circom language. This tool helps developers and users ensure the security and integrity of their ZKP projects by analyzing the source code and identifying potential issues during circuit design.


## Features

Circheck detects a variety of potential issues in Circom circuits, including:

- **Unconstrained Output Signals**: Detects output signals that are not constrained by any constraints.
- **Unconstrained Component Inputs**: Identifies input signals to components that are not constrained and may accept unchecked values.
- **Data Flow Constraint Discrepancy**: Finds signals that depend on others via dataflow but lack corresponding constraint dependencies.
- **Unused Component Outputs**: Warns when outputs of components are not used or checked in the circuit.
- **Unused Signals**: Identifies signals that are declared but never used in any computation or constraint.
- **Type Mismatch**: Detects potential type mismatches, such as signals flowing into templates like `Num2Bits` without proper range checks.
- **Assignment Misuse**: Finds assignment misuse, where a variable is assigned using the wrong operator.
- **Divide by Zero**: Warns of potential divide-by-zero issues in the circuit.
- **Non-deterministic Data Flow**: Flags conditional assignments depending on signals, which may lead to non-deterministic data flows.

## Installation

To install Circheck, you can clone the repository and install the required dependencies:

```bash
git clone https://github.com/ZJU-Automated-Reasoning-Group/CirChecker
cd CirChecker
pip install -r requirements.txt
```

It is better to use a venv.


## Usage

You can use it via the command line interface (CLI) to analyze Circom code and generate reports.

### Command Line Arguments

- `input`: **Required** - The path to the Circom file you want to analyze.
- `--json`: **Optional** - If specified, the tool will output a JSON report to the given file. The output file must end with `.json`.

### Example Usage

1. **Basic Analysis:**
   To analyze a Circom file and print the report to the console:

   ```bash
   circheck path/to/your/file.circom
   ```

   This will run the analysis and display the results directly in the terminal.

2. **Generate JSON Report:**
   To analyze the Circom file and save the report in a JSON file:

   ```bash
   circheck path/to/your/file.circom --json path/to/output/report.json
   ```

   This will run the analysis and save the results in the specified JSON file.

### Example Output:

When you run the tool, you'll see progress information printed to the terminal, such as:

```bash
PS C:\Users\GAMING\Desktop\Capstone_Project> circheck .\demo.circom --json .\result.json
[Info]       Generating AST for: .\demo.circom
[Success]    AST generated successfully.
[Success]    Type checking passed.
[Info]       Creating CDG: SingleAssignment0, in .\demo.circom
[Info]       Building conditional dependency edges of SingleAssignment0...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<?, ?it/s]
[Info]       Building condition constraint edges of SingleAssignment0...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<?, ?it/s]
[Success]    CDG created successfully.
[Info]       Starting the analysis process of graph SingleAssignment0.
[Info]       Detecting unconstrainted output...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<?, ?it/s]
[Info]       Detecting unconstrained component input...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<?, ?it/s]
[Info]       Detecting data flow constraint discrepancy...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████| 3/3 [00:00<?, ?it/s]
[Info]       Detecting unused component output...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<?, ?it/s]
[Info]       Detecting type mismatch...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<?, ?it/s]
[Info]       Detecting assignment misuse...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<?, ?it/s]
[Info]       Detecting unused signals...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<?, ?it/s]
[Info]       Detecting nondeterministic data flow...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<?, ?it/s]
[Success]    Detection completed successfully.
[Timeit]     Analysis completed in 0.30 s
```

If there are any warnings or issues detected, they will be printed like this:

```bash
[Warning]    In .\demo.circom:4:4
             Signal 'out' depends on 'a' via dataflow, but there is no corresponding constraint dependency.
[Warning]    In .\demo.circom:5:4
             Variable out is assigned using <-- instead of <==.
⚠ Total warnings: 2
```

### Example JSON Output:

If you specify a JSON output file, the results will also be saved to the file. For example:

```bash
[Success] Saved report to path/to/output/report.json
```

The JSON file will contain detailed information about the analysis, including detected vulnerabilities. A sample JSON output might look like this:

```json
{
  "SingleAssignment0": {
    "data flow constraint discrepancy": {
      ".\\demo.circom:4:4": [
        "Signal 'out' depends on 'a' via dataflow, but there is no corresponding constraint dependency."
      ]
    },
    "assignment missue": {
      ".\\demo.circom:5:4": [
        "Variable out is assigned using <-- instead of <==."
      ]
    }
  }
}
```

## Ack

Based on https://github.com/dangduongminhnhat/Circheck
