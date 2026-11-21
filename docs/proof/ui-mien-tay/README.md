# Bằng chứng: giao diện "Sông nước Miền Tây"

Chỉ đổi lớp vẽ `chonoi/web/index.html` (canvas tự vẽ, không asset ngoài); luật, contract v1.3, headless không đổi.
Giữ nguyên: logic phím/poll, 3 cảnh báo + tương phản cao, `getItemInfo`/độ tươi, hàm vẽ Cá Sấu của TV5.

| Ảnh | Cách tạo |
|---|---|
| `gather.png` | `python3 -m chonoi.live --mode gather --scenario docs/proof/ui-mien-tay/sc-gather.json` |
| `quan.png` | `python3 -m chonoi.live --mode quan --scenario docs/proof/ui-mien-tay/sc-quan.json` |
| `high-contrast-warnings.png` | `--mode gather --scenario docs/proof/phase-4/warn-gather.json`, mở `/?contrast=high` |
| `shop.png`, `done.png` | snapshot Shop / kết thúc dựng tay (mode `day` chưa nhận `--scenario`) |

Chụp bằng Chrome headless 1280×720, chỉ cửa sổ game. Kiểm tra: `node --check` phần `<script>` OK; unittest 115/115 OK.
