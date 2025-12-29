from flask import Flask, render_template, request
import random

app = Flask(__name__)

# -----------------------------
# 로또 번호 생성 함수
# -----------------------------
def generate_lotto(strategy):
    numbers = set()

    if strategy == "spread":
        # 홀수 위주 (고르게 분산된 느낌)
        while len(numbers) < 6:
            numbers.add(random.choice(range(1, 46, 2)))
    else:
        while len(numbers) < 6:
            n = random.randint(1, 45)
            if strategy == "no_birthday" and n <= 31:
                continue
            numbers.add(n)

    return sorted(numbers)

# -----------------------------
# 메인 페이지
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    # ===== 로또 상태 =====
    lotto_results = []
    probability = 0.0

    # ===== 구구단 상태 =====
    a = None
    b = None
    feedback = None
    game_active = False
    game_message = "게임을 시작하려면 버튼을 누르세요."

    if request.method == "POST":
        form_type = request.form.get("form_type")

        # ----------------- 로또 처리 -----------------
        if form_type == "lotto":
            strategy = request.form.get("strategy", "random")
            action = request.form.get("action")
            count = 1 if action == "single" else 10

            for _ in range(count):
                lotto_results.append(generate_lotto(strategy))

            probability = len(lotto_results) / 8145060 * 100

        # ----------------- 구구단 처리 -----------------
        elif form_type == "gugudan":
            action = request.form.get("action")

            # 게임 시작
            if action == "start":
                game_active = True
                a = random.randint(2, 9)
                b = random.randint(1, 9)
                game_message = "문제를 풀어보세요! (종료하려면 q 입력)"

            # 답 제출
            elif action == "answer":
                game_active = request.form.get("game_active") == "true"
                a = int(request.form.get("a"))
                b = int(request.form.get("b"))
                user_input = request.form.get("answer")

                if user_input.lower() == "q":
                    game_active = False
                    game_message = "게임이 종료되었습니다."
                else:
                    correct = a * b
                    if user_input.isdigit() and int(user_input) == correct:
                        feedback = "✅ 정답입니다!"
                    else:
                        feedback = f"❌ 틀렸어요. 정답은 {correct} 입니다."

                    # 다음 문제 자동 생성
                    a = random.randint(2, 9)
                    b = random.randint(1, 9)

    return render_template(
        "index.html",
        lotto_results=lotto_results,
        probability=probability,
        a=a,
        b=b,
        feedback=feedback,
        game_active=game_active,
        game_message=game_message
    )

if __name__ == "__main__":
    app.run(debug=True)
