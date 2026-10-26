# Áo jersey New York Brunson #11 Champions (chữ vàng) — brief

## Phân tích sản phẩm

- **Sản phẩm:** áo bóng rổ ba lỗ màu trắng, viền cổ và nách sọc xanh dương + cam. Mặt trước "NEW YORK" và số 11 **chữ vàng viền xanh**, patch cúp vàng ở ngực trái. Mặt sau "BRUNSON" và số 11 vàng, patch tròn "2025-26 Champions" dưới cổ. Nhãn vải "ONCE A KNICK, ALWAYS A KNICK".
- **Lưu ý ảnh:** cúp vàng và huy hiệu "2025-26 Champions" lớn ở góc dưới là hình minh hoạ, **không** gắn ở đó trên áo.
- **Bằng chứng 3 giây:** chữ vàng loé sáng dưới đèn + lưng áo "BRUNSON 11" → bản "gold edition" nhìn là thấy khác áo thường.
- **Người mua:** (1) fan bóng rổ New York 16-40, mê streetwear, văn hoá hype — mặc đi xem trận, đi bar, ra phố; (2) người mua tặng fan cứng (sinh nhật, Giáng sinh).
- **Góc bán:** ⭐ Flex chiến thắng kiểu NYC "gang gang" (chữ vàng, năng lượng đường phố) · Bản vàng giới hạn khác áo thường · Quà cho fan New York.
- **Không nhắc (chưa biết):** chất liệu, size, giá, ship, thêu hay in, hàng chính hãng hay không, **đội có thực sự vô địch 2025-26 không**. Chỉ nói thứ thấy trên áo: tên, số, chữ vàng, patch "2025-26 Champions".
- **Thương hiệu:** áo có logo NBA, Nike, nhận diện đội → prompt mô tả hình, không gọi tên; quảng cáo trả phí trên TikTok/Meta dễ bị từ chối, dùng nội bộ / organic thì ổn.

## Đã duyệt: hướng 1 — 8 nhát cắt (26/10/2026)

Rap, không tiếng gốc, 4 clip Veo; mỗi clip được viết thành **2 nửa có hành động khác nhau** (0-4s và 4-8s), Agent 2 lấy mỗi nửa làm một nhát → 8 nhát ~2s, xen kẽ clip, cắt trúng beat, drop nhạc rơi vào cú úp rổ.

| Shot | Clip | Nửa | Hình | Chữ slam |
|---|---|---|---|---|
| s01 | c01 | đầu | đi về phía camera trên phố đêm | NEW YORK |
| s02 | c03 | đầu | ánh sáng quét qua chữ vàng NEW YORK | GOLD EDITION |
| s03 | c02 | đầu | lưng áo BRUNSON 11 | BRUNSON 11 |
| s04 | c04 | đầu | rê bóng trên sân đêm | — |
| s05 | c03 | sau | patch cúp vàng, số 11 | 2025-26 CHAMPIONS |
| s06 | c04 | sau | úp rổ, bạn bè ùa vào, kim tuyến vàng (drop nhạc) | — |
| s07 | c02 | sau | xoay người lại nhìn ống kính | — |
| s08 | c01 | sau | dừng, kéo áo khoe chữ, hất cằm | GET YOURS — LINK BELOW ↓ |

Không cần nâng cấp "cắt nhanh" cho Agent 2: nửa sau của mỗi clip lấy bằng `override.src_in`.

## Story draft ban đầu (hướng 16 nhát, không dùng)

**Format:** Veo 3.1 · 9:16 · ~15s · **4 clip B-roll, không thoại, tắt tiếng gốc** · NYC đường phố đêm, đèn neon, ánh vàng · genre hype montage cắt nhanh
**Why this, here, now:** đêm ăn mừng ở New York, anh ấy mặc áo bản vàng ra phố, ra sân bóng rổ, cả khu phố ăn mừng.
**Nhạc:** rap NY drill / hard rap, có lời rap cũng được (không dùng tiếng gốc clip). Agent tự tìm.

### Cách dựng: 4 clip → ~16 nhát cắt

Mỗi clip Veo 8 giây được thiết kế có **nhiều khoảnh khắc khác nhau** (đi, quay người, cận chi tiết, nhảy ăn mừng). Agent 2 cắt mỗi clip thành 3-5 đoạn ngắn, **mỗi đoạn dài 2 beat nhạc** (~0.8-1s), xen kẽ các clip, cắt đúng beat. Cụm chữ to "slam" vào đúng các beat mạnh.

| Clip | Bối cảnh (8s) | Các khoảnh khắc để cắt |
|---|---|---|
| c01 | phố NYC đêm, đèn neon, hơi nước cống, góc thấp | anh ấy đi về phía camera đầy tự tin → dừng, kéo vạt áo khoe chữ vàng → hất cằm nhìn ống kính |
| c02 | cùng con phố, camera đứng sau lưng | anh ấy quay lưng, "BRUNSON 11" chiếm khung → xoay người lại 180° → nhìn ống kính |
| c03 | cận chi tiết áo dưới đèn đường | ánh sáng quét qua chữ vàng NEW YORK → patch cúp vàng → số 11 lấp lánh |
| c04 | sân bóng rổ ngoài trời ban đêm, đèn pha | anh ấy rê bóng → úp rổ/ném → ăn mừng cùng bạn bè, giấy kim tuyến vàng bay |

**Nhịp dựng (dự kiến, ~15s):**

| Thời gian | Nội dung | Chữ slam |
|---|---|---|
| 0-2s | c01 đi về phía camera ×2 nhát, c03 chữ vàng loé | NEW YORK |
| 2-5s | c02 lưng áo, c02 xoay người, c03 số 11 | BRUNSON 11 |
| 5-8s | c04 rê bóng, c01 kéo áo khoe, c03 patch cúp | GOLD EDITION |
| 8-11s | c04 úp rổ (trúng drop nhạc), c02 nhìn ống kính, c04 ăn mừng | 2025-26 CHAMPIONS |
| 11-15s | c04 kim tuyến vàng, c01 hất cằm nhìn ống kính + nút CTA | GET YOURS — LINK BELOW ↓ |

**Chi phí gen:** 4 keyframe + 4 clip × 8s (không đổi so với video thường; nhịp nhanh đến từ cách cắt).
**Cần nâng cấp Agent 2:** chế độ "cắt nhanh": cho nhiều đoạn lấy từ cùng một clip mà không trùng nhau, và đo độ dài cảnh bằng số beat thay vì giây. Mình làm phần này khi viết prompt.

**Hướng khác:**
1) **Ít nhát cắt hơn (6-8 nhát):** vẫn rap, nhưng mỗi cảnh ~2s, dễ xem chi tiết áo hơn.
2) **Flex trong phòng thay đồ/gương:** một người, khoe áo trước gương, cắt nhanh — rẻ hơn vì 1 bối cảnh.
