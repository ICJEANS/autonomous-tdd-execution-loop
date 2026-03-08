import argparse
from tdd_loop import run_loop

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    args = ap.parse_args()
    ok, logs = run_loop(args.target)
    for n, code, out in logs:
        print(f"=== attempt {n} / exit {code} ===")
        print(out)
    print("모든 테스트 통과 완료" if ok else "실패: 재시도 종료")

if __name__ == "__main__":
    main()
