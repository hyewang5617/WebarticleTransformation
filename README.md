# WebarticleTransformation
기사 본문 웹기사 형식으로 바꾸기

## 사용법

`scripts/convert_article.py`는 원문 텍스트를 CMS(CKEditor)용 HTML로 변환한다.

```
python scripts/convert_article.py examples/hitech_building.txt > output.html
```

### 입력 파일 작성 규칙 (`.txt`)

- 첫 문단: 리드(전문) 문단
- `## 소제목`: 18px 굵은 소제목으로 변환
- 빈 줄로 구분된 문단: 14px 본문 `<p>`로 변환 (한 블록 안의 줄바꿈은 화자가 바뀌는 인용처럼 각각 별도 `<p>`가 됨)
- `![캡션]` 또는 `![캡션](이미지경로)`: 가운데 정렬 이미지 + 캡션(▲ 캡션) 블록으로 변환. 경로를 비워두면 나중에 CMS에 업로드 후 `src`만 채워 넣으면 됨
- `"..."`, `'...'`: 자동으로 여는/닫는 곡선 따옴표(`&ldquo;` 등)로 변환, `·`는 `&middot;`로 변환
- 파일 끝 `---` 다음 줄부터 `이름|이메일` 형식으로 기자 바이라인 작성 (우측 정렬, 굵게)

예시 입력은 [examples/hitech_building.txt](examples/hitech_building.txt), 결과 HTML은 [examples/hitech_building.html](examples/hitech_building.html) 참고.

