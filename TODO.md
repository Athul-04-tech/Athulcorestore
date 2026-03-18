# Fix Cart Update/Delete (Non-AJAX Forms)

## Steps:
- [ ] 1. Update customer/views.py: Simplify views to always redirect, remove AJAX logic
- [ ] 2. Update usercart.html: Add forms/CSRF, remove JS
- [ ] 3. Update usercheckout.html: Add forms/CSRF for qty
- [ ] 4. Test: runserver, verify qty change/delete reloads correctly with messages

✅ 1. Update customer/views.py: Simplified views to always redirect, added item_total, removed AJAX logic

✅ 2. usercart.html: Forms for update/delete, CSRF, no JS needed (reloads page)

✅ 3. usercheckout.html: Qty forms added (page reloads to cart on update)

All edits complete. Ready for testing.
