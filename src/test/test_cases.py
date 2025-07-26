import os
import sys
import time
from datetime import datetime

locpath = [
    '../circheck/parser/',
    '../circheck/astgen/',
    '../circheck/typecheck/',
    '../circheck/utils/',
    '../circheck/cdggen/',
    '../circheck/detect/',
    '../circheck/',
    '../circheck/target/'
]

for p in locpath:
    if p not in sys.path:
        sys.path.append(p)


def test_bugs():
    benchmarks_dir = "../../benchmarks"
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    log_per_file = os.path.join(os.path.dirname(__file__), "log_per_file.txt")
    log_per_project = os.path.join(
        os.path.dirname(__file__), "log_per_project.txt")
    fails = []
    success = 0
    count = 0

    # checked already
    done_dir = [
        "aes-circom",
        "circom-ecdsa",
        "circom-matrix",
        "circom-ml",
        "circom-pairing",
        "circomlib-cff5ab6",
        "darkforest-eth-9033eaf",
        "ed25519-099d19c",
        "hermez-network-9a696e3-fixed",
        "hydra-2010a65",
        "iden3-core-56a08f9",
        "internal",
        "keccak256-circom-af3e898",
        "knownbug",
        "maci-9b1b1a6-fixed",
        "semaphore-0f0fc95",
        "zk-group-sigs-1337689-fixed",
        "zk-SQL-4c3626d",
        "zk-SQL-4c3626d"
    ]

    # Because it's cause time out or recursive many times.
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

    total_start = time.time()
    with open(log_per_file, "w") as f_filelog, open(log_per_project, "w") as f_projlog:
        f_filelog.write(f"[Per-file log generated at {datetime.now()}]\n\n")
        f_projlog.write(f"[Per-project log generated at {datetime.now()}]\n\n")
        for root, dirs, files in os.walk(benchmarks_dir):
            if 'libs' in dirs:
                dirs.remove('libs')

            subdir_name = os.path.basename(root)
            if subdir_name in done_dir:
                continue
            subdir_results_dir = os.path.join(results_dir, subdir_name)
            if not os.path.exists(subdir_results_dir):
                os.makedirs(subdir_results_dir)

            bug_files = [os.path.join(root, file) for file in files if file.endswith(
                ".circom") and file not in file_not_check]

            f_projlog.write(f"[PROJECT: {subdir_name}]\n")
            project_success = 0
            project_fail = 0
            project_start = time.time()

            for file_path in bug_files:
                # if "matPow_test.circom" not in file_path:
                #     continue
                print(f"[Info]       Running analysis for {file_path}")
                file_start = time.time()
                graphs, reports = detect(file_path)
                file_end = time.time()
                duration = file_end - file_start
                if graphs:
                    report_to_file(graphs, reports, os.path.join(
                        subdir_results_dir, f"{os.path.basename(file_path)}_report.json"))
                    success += 1
                    project_success += 1
                    f_filelog.write(f"[OK]   {file_path} in {duration:.2f}s\n")
                else:
                    fails.append(file_path)
                    project_fail += 1
                    f_filelog.write(f"[FAIL] {file_path} in {duration:.2f}s\n")
                print("---------------------------------------------")
            count += 1
            # if count == 2:
            #     break

            project_end = time.time()
            project_time = project_end - project_start
            project_total = project_success + project_fail
            avg = (project_time / project_total) if project_total else 0

            f_projlog.write(f"- Total files: {project_total}\n")
            f_projlog.write(f"- Success: {project_success}\n")
            f_projlog.write(f"- Failed: {project_fail}\n")
            f_projlog.write(f"- Time: {project_time:.2f}s\n")
            f_projlog.write(f"- Avg time per file: {avg:.2f}s\n\n")

        print(fails)
        total_end = time.time()
        total_time = total_end - total_start
        total_files = success + len(fails)
        print("[Summary]")
        print(f"- Total files: {success + len(fails)}")
        print(f"- Success: {success}")
        print(f"- Failed: {len(fails)}")
        print(f"- Total time: {total_time:.2f} seconds")
        print(f"- Avg time per file: {total_time / success:.2f} seconds")

        f_projlog.write("[OVERALL SUMMARY]\n")
        f_projlog.write(f"- Total files: {total_files}\n")
        f_projlog.write(f"- Success: {success}\n")
        f_projlog.write(f"- Failed: {len(fails)}\n")
        f_projlog.write(f"- Total time: {total_time:.2f}s\n")
        f_projlog.write(
            f"- Avg time per file: {total_time / total_files:.2f}s\n")


if __name__ == "__main__":
    from core import detect, report_to_file

    test_bugs()
