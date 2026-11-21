# TEAM

**Tên nhóm:** 439  **Số người:** 5  (khớp `team_size` trong `game.contract.json`)

| Thành viên | GitHub handle | Module chính | Vai quy trình | Người dự phòng cho |
|---|---|---|---|---|
| Hoàng Thế Phong (Lead) | phong | `sim/gather` | Team Lead, PO/Integrator | Nguyễn Hồng Thắng |
| Nguyễn Hồng Thắng (Gather) | thangdktd | `sim/gather` | Developer Gather | Hoàng Thế Phong |
| Đào Văn Hiệp (Quán) | daohiep2903 | `sim/quan` | Developer Quán | Nguyễn Trọng Lâm |
| Nguyễn Trọng Lâm (Quán) | NTLam108 | `sim/quan` | Developer Quán | Đào Văn Hiệp |
| Vũ Xuân Hiếu (QA/HUD) | vuhieuvh | `qa` | QA Lead + HUD | Hoàng Thế Phong |

**Vai quy trình:** PO (đầu mối hỏi giảng viên, giữ `docs/clarify.md`) · Integrator (giữ `docs/contracts/`, gắn tag) · QA lead · Scrum/Release. Có thể kiêm.

## Thỏa thuận làm việc nhóm (chốt T+0–15)

- Kênh liên lạc: Discord / Zalo 439.
- Khi bất đồng về thiết kế: Trao đổi nhanh ≤ 2 phút; nếu chưa thống nhất thì Integrator (Hoàng Thế Phong) quyết định theo Test Contract và ghi lại lý do.
- Khi ai đó trễ hoặc vướng quá 10 phút: Báo ngay lên kênh chung, người dự phòng lập tức nhận việc hỗ trợ.
- Giờ standup: T+20 rà soát blocker giữa Phase 1.
- Phân chia quyền sở hữu file: Hoàng Thế Phong/Nguyễn Hồng Thắng phụ trách `gather.py`, Đào Văn Hiệp/Nguyễn Trọng Lâm phụ trách `quan.py`, Vũ Xuân Hiéu phụ trách test/HUD/docs.
- Cách làm việc với Git: Mỗi người code trên lát của mình, rebase/merge vào `main`, Hoàng Thế Phong kiểm tra tích hợp và gắn tag `phase-1` trước T+60.
