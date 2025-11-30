from django.core.management.base import BaseCommand
from board.models import CommunityBoard


class Command(BaseCommand):
    help = '커뮤니티 게시판의 초기 카테고리(자유, 질문, 토론)를 생성합니다.'

    def handle(self, *args, **kwargs):
        # 생성할 게시판 목록 정의 (제목, 타입코드)
        boards_data = [
            ("자유", "free"),
            ("질문", "qna"),
            ("토론", "discussion")
        ]

        self.stdout.write("게시판 데이터 생성을 시작합니다..."

        created_count = 0
        for title, type_code in boards_data:
            # get_or_create: 데이터가 없으면 만들고, 있으면 가져옵니다. (중복 방지)
            board, created = CommunityBoard.objects.get_or_create(
                board_title=title,
                board_type=type_code
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ 생성됨: {title} ({type_code})"))
                created_count += 1
            else:
                self.stdout.write(self.style.WARNING(f"ℹ️ 이미 존재함: {title} ({type_code})"))

        if created_count > 0:
            self.stdout.write(self.style.SUCCESS(f"\n총 {created_count}개의 게시판이 새로 생성되었습니다."))
        else:
            self.stdout.write(self.style.SUCCESS("\n모든 게시판이 이미 존재합니다. 추가 작업이 필요 없습니다."))