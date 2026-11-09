import argparse
from dataclasses import dataclass
import json

@dataclass
class Step:
    key: str
    title: str
    prompt: str

STEPS = [
    Step('validate', '验证', 'What problem and target users?'),
    Step('bp', 'BP', 'What is the one-page business plan?'),
    Step('policy', '政策', 'Any compliance or policy risks?'),
    Step('pitch', '路演', 'What is the 30-second pitch?'),
    Step('growth', '获客', 'What is the first acquisition channel?'),
    Step('pricing', '定价', 'What is the pricing hypothesis?'),
    Step('register', '注册', 'What entity and jurisdiction?'),
]

def collect(steps):
    answers = {}
    for i, step in enumerate(steps, 1):
        print(f'[{i}/{len(steps)}] {step.title}: {step.prompt}')
        answers[step.key] = input('> ').strip() or 'TBD'
    return answers

def score(answers):
    filled = sum(v != 'TBD' for v in answers.values())
    return round(filled / len(answers) * 100)

def render(answers):
    lines = ['# AI Startup 7-Step Skill Report', '']
    for step in STEPS:
        lines.append(f'## {step.title}')
        lines.append(answers[step.key])
        lines.append('')
    lines.append(f'Completion score: {score(answers)}%')
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description='AI startup 7-step skill demo')
    parser.add_argument('--json', action='store_true', help='output JSON')
    args = parser.parse_args()
    answers = collect(STEPS)
    if args.json:
        print(json.dumps({'answers': answers, 'score': score(answers)}, ensure_ascii=False, indent=2))
    else:
        print(render(answers))

if __name__ == '__main__':
    main()