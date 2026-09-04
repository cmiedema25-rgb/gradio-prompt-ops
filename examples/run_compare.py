from gradio_prompt_ops.compare import compare_prompts
from gradio_prompt_ops.rubric import Rubric

LOAD = (
    "Load LW-441 from Chicago to Dallas is 6 hours late. "
    "Driver cited traffic. Customer is Cascadia."
)


def main() -> None:
    pair = compare_prompts(
        "Write a creative punchy customer update.",
        "Write a concise ops update. Do not promise ETAs. Do not invent facts.",
        LOAD,
        Rubric(required_terms=["LW-441", "6"], forbidden_terms=["guarantee"]),
    )
    print(pair.winner, pair.score_a.score, pair.score_b.score)
    print(pair.output_b)


if __name__ == "__main__":
    main()
