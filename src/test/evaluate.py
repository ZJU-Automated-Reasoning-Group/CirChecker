import csv
import json
import os
import pandas as pd

output_file = 'evaluation.csv'
results_dir = os.path.join(os.path.dirname(__file__), "results")
TP = TN = FP = FN = 0
TP_circomspect = TN_circomspect = FP_circomspect = FN_circomspect = 0
TP_zkap = TN_zkap = FP_zkap = FN_zkap = 0

output_rows = []
file = open("zkap.txt", "r")
data = file.readline()

file_not_check = [
    "ECDSAVerifyNoPubkeyCheck@circom-ecdsa@n=64@k=4.circom",
    "secp256k1ScalarMult@circom-ecdsa@n=64@k=4.circom",
    "mnist_convnet_test.circom",
    "mnist_test.circom",
    "Ark@poseidon.circom",
    "BabyPbk@babyjub.circom",
    "Bits2Point_Strict@pointbits.circom",
    "Poseidon@poseidon.circom",
    "Sigma@poseidon.circom",
    "CoreVerifyPubkeyG1@circom-pairing@n=55@k=7.circom",
    "batchverify.circom",
    "inversemodulo1.circom",
    "modulus0.circom",
    "modulus2.circom",
    "modulusq2.circom",
    "verify.circom",
    "test-decode-tx.circom",
    "test-fee-tx.circom",
    "test-hash-inputs.circom",
    "test-rollup-main-L1.circom",
    "test-rollup-tx-states.circom",
    "test-rollup-tx.circom",
    "test-withdraw.circom",
    "hydra-s1.circom",
    "verify-hydra-commitment.circom",
    "verify-merkle-path.circom",
    'auth.circom',
    'authTest.circom',
    'authWithRelayTest.circom',
    'credentialAtomicQueryMTP.circom',
    'credentialAtomicQueryMTPTest.circom',
    'credentialAtomicQueryMTPWithRelay.circom',
    'credentialAtomicQueryMTPWithRelayTest.circom',
    'micQueryMTPWithRelay.cicredentialAtomicQuerySig.circom',
    'credentialAtomicQuerySigTest.circom',
    'idOwnershipBySignatureWithRelayTest.circom',
    'poseidon.circom',
    'iden3-coreWithRelayTest.circom',
    'poseidon14.circom',
    'poseidon16.circom',
    'stateTransition.circom',
    'stateTransitionTest.circom',
    'utils_checkIdenStateMatchesRoots.circom',
    'utils_getClaimEcircom',
    'benchmaxpiration.circom',
    'utils_getClaimSubjectOtherIden.circom',
    'utils_getSubjectLocation.circom',
    'utils_GetValueByIndex.circom',
    'utils_isExpirable.circom',
    'utils_isUpdatabldatable.circom',
    'utils_verifyClaimSignature.circom',
    'utils_verifyCredentialSubject.circom',
    'utils_verifyExpirationTime.circom',
    "credentialAtomicQuerySig.circom",
    "idOwnershipBySignatureTest.circom",
    "utils_getClaimExpiration.circom",
    "utils_isUpdatable.circom",
    "Rotate@telepathy.circom",
    "absorb_test.circom",
    "final_test.circom",
    "keccakf_test.circom",
    "keccak_256_256_test.circom",
    "keccak_32_256_test.circom",
    "batchUpdateStateTree_32.circom",
    "batchUpdateStateTree_32_batch16.circom",
    "batchUpdateStateTree_32_batch256.circom",
    "batchUpdateStateTree_large.circom",
    "batchUpdateStateTree_medium.circom",
    "batchUpdateStateTree_small.circom",
    "batchUpdateStateTree_test.circom",
    "hasher11_test.circom",
    "hasher5_test.circom",
    "hashleftright_test.circom",
    "merkleTreeCheckRoot_test.circom",
    "merkleTreeInclusionProof_test.circom"
    "merkleTreeLeafExists_test.circom",
    "merkleTreeLeafExists_test.circom",
    "merkleTreeInclusionProof_test.circom",
    "performChecksBeforeUpdate_test.circom",
    "quadVoteTally_32.circom",
    "quadVoteTally_32_batch16.circom",
    "quadVoteTally_32_batch256.circom",
    "quadVoteTally_large.circom",
    "quadVoteTally_medium.circom",
    "quadVoteTally_small.circom",
    "quadVoteTally_test.circom",
    "quinGeneratePathIndices_test.circom",
    "quinSelector_test.circom",
    "quinTreeCheckRoot_test.circom",
    "quinTreeInclusionProof_test.circom",
    "quinTreeLeafExists_test.circom",
    "resultCommitmentVerifier_test.circom",
    "splicer_test.circom",
    "updateStateTree_test.circom",
    "verifySignature_test.circom",
    "semaphore.circom",
    "delete.circom",
    "insert.circom",
    "select.circom",
    "update.circom",
    "hashTable.circom",
    "utils.circom"
]

CIRCHECK_TO_ZKAP = {
    "unconstrained_output": "Unconstrained Circ. Output",
    "unconstrained component input": "Unconstrained Comp. Input",
    "data flow constraint discrepancy": "Dataflow-constraint Discrepancy",
    "unused component output": "Unused Comp. Output",
    "unused signal": "Unused Circ. Signal",
    "divide by zero": "Division-By-Zero",
    "nondeterministic data flow": "Non-Deterministic-Dataflow",
    "type mismatch": "Type-Mismatch",
    "assignment missue": "Assignment misuse"
}

ZKSOLID_BUGS = ["UCO", "USCI", "DCD", "TM", "US", "USCO", "AM", "NDD", "DBZ"]
ZKSOLID_TO_CIRCHECK = {
    "UCO": "unconstrained_output",
    "USCI": "unconstrained component input",
    "DCD": "data flow constraint discrepancy",
    "TM": "type mismatch",
    "US": "unused signal",
    "USCO": "unused component output",
    "AM": "assignment missue",
    "NDD": "nondeterministic data flow",
    "DBZ": "divide by zero"
}

ZKAP_TO_CIRCHECK = {v: k for k, v in CIRCHECK_TO_ZKAP.items()}

all_bug_types = list(CIRCHECK_TO_ZKAP.keys())
vul_stats = {bug: {'TP': 0, 'FP': 0, 'FN': 0, 'TN': 0}
             for bug in all_bug_types}
zksolid_bug_stats = {bug: {'TP': 0, 'FP': 0, 'FN': 0, 'TN': 0}
                     for bug in ZKSOLID_BUGS}

while data:
    col = data.split(",")
    name, project, groundtruth, circomspect, zkap = col[0], col[1], col[10], col[11], col[12]
    expected_detetector = col[2:7]
    circheck_bugs = set()
    zkap = zkap.replace("\n", "")
    if name in file_not_check:
        data = file.readline()
        continue
    name = name + "_report.json"
    if project == "circomlib":
        project = "circomlib-cff5ab6"
    if project == "iden3-core-56a08f20" or project == "iden3-core-56a08f24":
        project = "iden3-core-56a08f9"
    if "keccak256" in project:
        project = "keccak256-circom-af3e898"
    json_path = results_dir + "\\" + project + "\\" + name

    result = 'file not found'

    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as jf:
            try:
                data = json.load(jf)
                if data == {}:
                    result = 'safe'
                else:
                    result = 'unsafe'
                    for circuit_name, circuit_issues in data.items():
                        for issue_type, locations in circuit_issues.items():
                            circheck_bugs.add(issue_type)
            except json.JSONDecodeError:
                result = 'invalid json'
        if groundtruth == 'unsafe' and result == 'unsafe':
            TP += 1
        elif groundtruth == 'safe' and result == 'safe':
            TN += 1
        elif groundtruth == 'safe' and result == 'unsafe':
            FP += 1
            # print("+++ false positive =", json_path)
        elif groundtruth == 'unsafe' and result == 'safe':
            FN += 1
            # print("--- false negative =", json_path)

        if groundtruth == 'unsafe' and circomspect == 'unsafe':
            TP_circomspect += 1
        elif groundtruth == 'safe' and circomspect == 'safe':
            TN_circomspect += 1
        elif groundtruth == 'safe' and circomspect == 'unsafe':
            FP_circomspect += 1
        elif groundtruth == 'unsafe' and circomspect == 'safe':
            FN_circomspect += 1

        if groundtruth == 'unsafe' and zkap == 'unsafe':
            TP_zkap += 1
        elif groundtruth == 'safe' and zkap == 'safe':
            TN_zkap += 1
        elif groundtruth == 'safe' and zkap == 'unsafe':
            FP_zkap += 1
            # print("+++ false positive - zkap =", json_path)
        elif groundtruth == 'unsafe' and zkap == 'safe':
            FN_zkap += 1
            # print("--- false negative - zkap =", json_path)

        if groundtruth in ["safe", "unsafe"]:
            for bug in all_bug_types:
                # if bug != "unconstrained_output":
                #     continue
                in_zkap = CIRCHECK_TO_ZKAP[bug] in expected_detetector
                in_circheck = bug in circheck_bugs

                if in_zkap and in_circheck:
                    vul_stats[bug]['TP'] += 1
                elif not in_zkap and in_circheck:
                    vul_stats[bug]['FP'] += 1
                    print("+++ false positive =", json_path, bug)
                elif in_zkap and not in_circheck:
                    vul_stats[bug]['FN'] += 1
                    print("--- false negative =", json_path, bug)
                elif not in_zkap and not in_circheck:
                    vul_stats[bug]['TN'] += 1

            zksolid_values = col[13:22]
            for i, bug_short in enumerate(ZKSOLID_BUGS):
                cir_bug = ZKSOLID_TO_CIRCHECK[bug_short]
                zkap_bug_name = CIRCHECK_TO_ZKAP[cir_bug]

                in_zkap = zkap_bug_name in expected_detetector
                in_zksolid = zksolid_values[i].strip().lower() == "unsafe"

                stats = zksolid_bug_stats[bug_short]
                if in_zkap and in_zksolid:
                    stats['TP'] += 1
                elif not in_zkap and in_zksolid:
                    print("+++ false positive - zkap =", json_path, bug_short)
                    stats['FP'] += 1
                elif in_zkap and not in_zksolid:
                    stats['FN'] += 1
                    print("--- false negative - zkap =", json_path, bug_short)
                else:
                    stats['TN'] += 1
    else:
        print("not found: ", json_path)

    data = file.readline()

file.close()


def evaluate(tp, tn, fp, fn):
    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total if total else 0
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = 2 * precision * recall / \
         (precision + recall) if (precision + recall) else 0
    fp_rate = fp / (fp + tn) if (fp + tn) else 0
    fn_rate = fn / (fn + tp) if (fn + tp) else 0
    return {
        "Total": total,
        "True Positive (TP)": tp,
        "True Negative (TN)": tn,
        "False Positive (FP)": fp,
        "False Negative (FN)": fn,
        "Accuracy": round(accuracy, 4),
        "Precision": round(precision, 4),
        "Recall": round(recall, 4),
        "F1-Score": round(f1, 4),
        "FP Rate": round(fp_rate, 4),
        "FN Rate": round(fn_rate, 4),
    }


circheck_stats = evaluate(TP, TN, FP, FN)
circomspect_stats = evaluate(
    TP_circomspect, TN_circomspect, FP_circomspect, FN_circomspect)
zkap_stats = evaluate(TP_zkap, TN_zkap, FP_zkap, FN_zkap)

for tool, stats in zip(["Circheck", "ZKAP", "CIRCOMSPECT"],
                       [circheck_stats, zkap_stats, circomspect_stats]):
    print(f"\n=== {tool} ===")
    for k, v in stats.items():
        print(f"{k}: {v}")

for bug_type, values in vul_stats.items():
    result = evaluate(values["TP"], values["TN"], values["FP"], values["FN"])
    print(f"\n=== {bug_type} ===")
    for k, v in result.items():
        print(f"{k}: {v}")

print("\n=== ZKAP Evaluation ===")
for bug, values in zksolid_bug_stats.items():
    result = evaluate(values["TP"], values["TN"], values["FP"], values["FN"])
    print(f"\nBug: {ZKSOLID_TO_CIRCHECK[bug]}")
    for k, v in result.items():
        print(f"{k}: {v}")
