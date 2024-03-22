import os
import re

from commitizen import defaults
from commitizen.cz.base import BaseCommitizen
from commitizen.cz.utils import multiple_line_breaker, required_validator
from commitizen.defaults import Questions

__all__ = ["ConventionalCommitsCz"]


def parse_message(text):
    if isinstance(text, str) and text != '':
        text = text.strip('.')
        text = (text[0].upper() + text[1:])

    return required_validator(text, msg="Message is required.")

def parse_scope(text):
    if not text:
        return ""

    scope = text.strip().split()
    if len(scope) == 1:
        return scope[0]

    return "-".join(scope)


def parse_subject(text):
    if isinstance(text, str):
        text = text.strip(".").strip()

    return required_validator(text, msg="Subject is required.")


class ConventionalCommitsCz(BaseCommitizen):
    bump_pattern = defaults.bump_pattern
    bump_map = defaults.bump_map
    bump_map_major_version_zero = defaults.bump_map_major_version_zero
    commit_parser = defaults.commit_parser
    change_type_map = {
        "feat": "Feat",
        "fix": "Fix",
        "refactor": "Refactor",
        "perf": "Perf",
    }
    changelog_pattern = defaults.bump_pattern

    def questions(self) -> Questions:
        questions: Questions = [
            {
                "type": "list",
                "name": "type",
                "message": "커밋하려는 변경 유형을 선택하세요.",
                "choices": [
                    {
                        "value": "Fix",
                        "name": "Fix: 버그를 수정할 때 사용합니다.",
                        "key": "x",
                    },
                    {
                        "value": "Feat",
                        "name": "Feat: 새로운 기능(feature)이 추가될 때 사용합니다.",
                        "key": "f",
                    },
                    {
                        "value": "Docs",
                        "name": "Docs: 문서(예: README, CHANGELOG, CONTRIBUTE 등)를 업데이트할 때 사용합니다.",
                        "key": "d",
                    },
                    {
                        "value": "Style",
                        "name": (
                            "Style: 코드 형식, 정렬 등과 같은 스타일을 변경할 때 사용합니다. (들여쓰기 같은 포맷이나 세미콜론을 빼먹은 경우)"
                        ),
                        "key": "s",
                    },
                    {
                        "value": "Refactor",
                        "name": (
                            "Refactor: 코드를 리팩토링했을 때 사용합니다. 즉, 기능 변경 없이 내부 구조를 개선할 때 사용합니다."
                        ),
                        "key": "r",
                    },
                    {
                        "value": "Perf",
                        "name": "Perf: 성능을 향상시키는 코드 변경 시 사용합니다.",
                        "key": "p",
                    },
                    {
                        "value": "Test",
                        "name": (
                            "Test: 테스트 코드를 추가하거나 기존 테스트를 수정할 때 사용합니다."
                        ),
                        "key": "t",
                    },
                    {
                        "value": "Build",
                        "name": (
                            "Build: 빌드 시스템 또는 외부 의존성과 관련된 변경사항에 사용합니다. (예: pip, docker, npm)"
                        ),
                        "key": "b",
                    },
                    {
                        "value": "Chore",
                        "name": (
                            "Chore: 자잘한 수정사항, 패키지 매니저 설정 등, 기타 유지보수 작업을 할 때 사용합니다."
                        ),
                        "key": "c",
                    },
                ],
            },
            {
                "type": "input",
                "name": "message",
                "message": (
                    "메시지를 입력하세요. (첫글자는 대문자로 변환됩니다. / 문장끝 '.'도 제거 됩니다.)\n"
                ),
                "filter": parse_message,
            },
        ]
        return questions

    def message(self, answers: dict) -> str:
        type = answers["type"]
        message = answers["message"]

        return f"{type}: {message}"

    def example(self) -> str:
        return (
            "Docs: Update README.md"
        )

    def schema(self) -> str:
        return (
            "<Type>: <Message>"
        )

    def schema_pattern(self) -> str:
        PATTERN = (
            r"^(Feat|Fix|Refactor|Style|Docs|Test|Chore|Perf|Build)"  # type
            r": (.+)$"  # message
        )
        return PATTERN

    def info(self) -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(dir_path, "conventional_commits_info.txt")
        with open(filepath, encoding=self.config.settings["encoding"]) as f:
            content = f.read()
        return content

    def process_commit(self, commit: str) -> str:
        pat = re.compile(self.schema_pattern())
        m = re.match(pat, commit)
        if m is None:
            return ""
        return m.group(3).strip()
