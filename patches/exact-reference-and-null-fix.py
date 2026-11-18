from pathlib import Path
import re
app=next(Path("appsrc").rglob("package.json")).parent
hp=app/"www"/"index.html"; jp=app/"www"/"app.js"
h=hp.read_text(encoding="utf-8"); s=jp.read_text(encoding="utf-8")

# Align the new markup with the IDs consumed by the existing application.
h=h.replace('id="paymentStatus"','id="status"').replace('for="paymentStatus"','for="status"')
if 'id="orderNotes"' not in h:
    h=h.replace('<input type="hidden" id="editId">','<input type="hidden" id="editId"><input type="hidden" id="orderNotes" value="">')
if 'id="currency"' not in h:
    h=h.replace('<input type="hidden" id="orderNotes" value="">','<input type="hidden" id="orderNotes" value=""><input type="hidden" id="currency" value="SAR">')
# Keep the contact picker available without adding a visible row absent from the approved screenshot.
h=h.replace('<label for="customerPhone">رقم الموبايل　☎</label><input id="customerPhone" inputmode="tel" placeholder="رقم الموبايل"><button type="button" class="contact-import-btn" id="pickContact">اختيار من الدليل</button>',
'<label for="customerPhone">رقم الموبايل　<button type="button" class="contact-icon-btn" id="pickContact" aria-label="اختيار من دليل الهاتف">☎</button></label><input id="customerPhone" inputmode="tel" placeholder="رقم الموبايل">')
css=r"""
#new .contact-icon-btn{border:0;background:transparent;color:#1269c8;font-size:1.3em;font-weight:bold;padding:0 4px}
#new .contact-import-btn{display:none!important}
#new .payment-state-field{display:none!important}
#saveSuccessOverlay{position:fixed;inset:0;z-index:100000;background:rgba(15,23,42,.42);display:flex;align-items:center;justify-content:center;padding:4vw;box-sizing:border-box}
#saveSuccessCard{position:relative;width:min(88vw,900px);max-height:92vh;overflow:auto;background:#fff;border-radius:5.5vw;box-shadow:0 18px 55px rgba(0,0,0,.24);padding:4.5vw 4.5vw 3vw;direction:rtl;color:#303747;font-family:Tahoma,Arial,sans-serif}
#saveSuccessCard .ss-head{display:flex;align-items:center;justify-content:space-between;gap:3vw;margin-bottom:2.4vw;min-height:12vw;padding:0 2vw}
#saveSuccessCard .ss-check{width:13vw;height:13vw;max-width:136px;max-height:136px;border-radius:50%;background:#dff7e9;color:#13a45b;display:grid;place-items:center;font-size:clamp(34px,8vw,82px);font-weight:bold;flex:none;box-shadow:0 0 0 1.8vw #e8f8ef}
#saveSuccessCard h3{font-size:clamp(22px,5vw,52px);margin:0;color:#07964b;font-weight:800;text-align:center}
#saveSuccessCard .ss-x{position:absolute;top:3vw;right:3vw;border:0;background:transparent;color:#778196;font-size:clamp(26px,5vw,52px);line-height:1}
#saveSuccessCard .ss-meta{display:grid;grid-template-columns:1fr;gap:0;margin:2vw 0 2.2vw;border-top:2px solid #dce3ed;padding-top:1.5vw}
#saveSuccessCard .ss-meta div{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:1.25vw .6vw;font-size:clamp(15px,3.7vw,36px)}
#saveSuccessCard small{color:#50596b;font-size:inherit;margin:0;font-weight:700}
#saveSuccessCard .ss-money{display:grid;gap:0;border:2px solid #c6ddf7;border-radius:2.5vw;overflow:hidden}
#saveSuccessCard .ss-title{background:#dceeff;color:#123b68;text-align:center;padding:1.2vw;font-size:clamp(18px,4vw,40px);font-weight:800}
#saveSuccessCard .ss-row{display:flex;justify-content:space-between;align-items:center;gap:10px;font-size:clamp(14px,3.3vw,32px);padding:1.35vw 1.6vw;border-bottom:1px solid #e0e8f2}
#saveSuccessCard .ss-num{direction:ltr;text-align:left;white-space:nowrap;font-weight:700}
#saveSuccessCard .ss-sale .ss-num{color:#125ec3}
#saveSuccessCard .ss-due{background:#ffedcb;color:#111;font-weight:800}
#saveSuccessCard .ss-due .ss-num{color:#f07800;font-size:1.3em}
#saveSuccessCard .ss-received .ss-num{color:#16a05b}
#saveSuccessCard .ss-remaining .ss-num{color:#e01b1b}
#saveSuccessCard .ss-currency{display:flex;justify-content:space-between;margin:2vw 0;font-size:clamp(15px,3.4vw,33px);padding:1vw 0;border-bottom:1px solid #d8e0eb}
#saveSuccessCard .ss-currency strong{font-size:1.2em;direction:ltr}
#saveSuccessCard .ss-close{width:100%;border:0;border-radius:2.6vw;background:linear-gradient(110deg,#1674d0,#0755a2);color:#fff;padding:2.3vw;font-weight:800;font-size:clamp(18px,4vw,40px)}
"""
h=h.replace("</style></head>",css+"\n</style></head>",1)

# Product rows include the computed line total, while preserving the existing item data shape.
start=s.index("function addItemRow("); end=s.index("\nfunction getItems()",start)
s=s[:start]+'''function addItemRow(item={name:'',qty:1,cost:0,price:0}){let d=document.createElement('div');d.className='itemline';d.innerHTML=`<input class="iname" placeholder="اسم الصنف" value="${esc(item.name)}"><input class="iqty" type="number" min="1" value="${item.qty}"><input class="icost" type="number" min="0" step="0.01" value="${item.cost}"><input class="iprice" type="number" min="0" step="0.01" value="${item.price}"><output class="lineTotal">${money(Number(item.qty||0)*Number(item.price||0),'').trim()}</output><button type="button" class="delItem" aria-label="حذف الصنف">▣</button>`;$('items').append(d);d.querySelectorAll('input').forEach(x=>x.addEventListener('input',()=>{updateLineTotal(d);calcSummary();}));d.querySelector('.delItem').onclick=()=>{d.remove();calcSummary();};updateLineTotal(d);calcSummary();}
function updateLineTotal(row){if(!row)return;const q=Number(row.querySelector('.iqty')?.value||0),p=Number(row.querySelector('.iprice')?.value||0),out=row.querySelector('.lineTotal');if(out)out.textContent=money(q*p,'').trim();}
''' + s[end:]

# Four-column financial summary, as in the approved reference.
start=s.index("function calcSummary()"); end=s.index("$('addItem').onclick",start)
s=s[:start]+'''function calcSummary(){let o={items:getItems(),shippingCost:$('shippingCost').value,shippingCharge:$('shippingCharge').value,currency:$('currency').value};let t=totals(o);$('orderSummary').innerHTML=`<div class="sum-grid"><div class="sum-item sum-cost"><small>إجمالي تكلفة البضاعة</small><b>${money(t.cost,o.currency)}</b></div><div class="sum-item sum-sale"><small>إجمالي بيع البضاعة</small><b>${money(t.sale,o.currency)}</b></div><div class="sum-item sum-shipping"><small>الشحن على العميل</small><b>${money(t.sh,o.currency)}</b></div><div class="sum-item sum-due"><small>المطلوب من العميل</small><b>${money(t.due,o.currency)}</b></div></div>;}
''' + s[end:]

# Correctly persist payment state and amount received, with strict validation.
start=s.index("function formData()"); end=s.index("$('reviewOrder').onclick",start)
s=s[:start]+'''function formData(){let items=getItems(),status=$('status').value;return {id:$('editId').value||('ORD-'+Date.now()),date:today(),customerName:$('customerName').value.trim(),customerPhone:$('customerPhone').value.trim(),currency:$('currency').value,status,paymentStatus:status,amountReceived:Number($('amountReceived').value||0),items,shippingCost:Number($('shippingCost').value||0),shippingCharge:Number($('shippingCharge').value||0),notes:$('orderNotes').value};}
function validate(o){if(!o.customerName)return 'أدخل اسم العميل';if(!o.items.length)return 'أضف صنفاً واحداً على الأقل';for(let x of o.items){if(!x.name||x.qty<1||x.cost<0||x.price<x.cost)return 'تحقق من بيانات الأصناف: سعر البيع لا يقل عن التكلفة';}if(o.shippingCost<0||o.shippingCharge<0)return 'قيمة الشحن لا يمكن أن تكون سالبة';let due=totals(o).due;if(o.amountReceived<0||o.amountReceived>due)return 'المبلغ المستلم لا يمكن أن يتجاوز المبلغ المطلوب';if(o.status==='بانتظار الدفع'&&o.amountReceived!==0)return 'في حالة انتظار الدفع يجب أن يكون المبلغ المستلم صفراً';if(o.status==='تم استلام جزء من المبلغ'&&!(o.amountReceived>0&&o.amountReceived<due))return 'أدخل مبلغاً مستلماً أكبر من صفر وأقل من المبلغ المطلوب';if(o.status==='تم استلام المبلغ بالكامل'&&o.amountReceived!==due)return 'عند استلام المبلغ بالكامل يجب أن يساوي المستلم إجمالي المطلوب';return '';}
''' + s[end:]

# Save directly and show the centered, reference-style success dialog only after IndexedDB confirms persistence.
start=s.index("$('reviewOrder').onclick="); end=s.index("$('backEdit').onclick",start)
s=s[:start]+'''$('reviewOrder').onclick=async()=>{let o=formData(),err=validate(o);if(err){alert(err);return;}try{let idx=orders.findIndex(x=>x.id===o.id);if(idx>=0)orders[idx]=o;else orders.unshift(o);await saveAll();clearForm();showPage('orders');showSavedOrderSummary(o);}catch(e){alert('تعذر حفظ الطلب: '+(e?.message||e));}};
''' + s[end:]

start=s.index("function clearForm()"); end=s.index("$('clearForm').onclick",start)
s=s[:start]+'''function clearForm(){$('editId').value='';$('formTitle').textContent='طلب جديد';['customerName','customerPhone','orderNotes'].forEach(x=>{if($(x))$(x).value='';});$('currency').value='SAR';$('status').value='بانتظار الدفع';$('amountReceived').value=0;$('shippingCost').value=0;$('shippingCharge').value=0;$('items').innerHTML='';addItemRow();calcSummary();}
function editOrder(id){let o=orders.find(x=>x.id===id);if(!o)return;showPage('new');$('editId').value=o.id;$('formTitle').textContent='تعديل الطلب';$('customerName').value=o.customerName;$('customerPhone').value=o.customerPhone;$('currency').value=o.currency;$('status').value=o.status||o.paymentStatus||'بانتظار الدفع';$('amountReceived').value=Number(o.amountReceived||0);$('shippingCost').value=o.shippingCost;$('shippingCharge').value=o.shippingCharge;$('orderNotes').value=o.notes||'';$('items').innerHTML='';o.items.forEach(addItemRow);calcSummary();}
''' + s[end:]

# The status selector remains internal to keep the screenshot faithful; values are synchronized with the received amount.
if "$('amountReceived').addEventListener('input'" not in s:
    s=s.replace("$('addItem').onclick=()=>addItemRow();", "$('addItem').onclick=()=>addItemRow();\n$('status').addEventListener('change',()=>{let due=totals({items:getItems(),shippingCost:$('shippingCost').value,shippingCharge:$('shippingCharge').value}).due;if($('status').value==='بانتظار الدفع')$('amountReceived').value=0;else if($('status').value==='تم استلام المبلغ بالكامل')$('amountReceived').value=due;});\n$('amountReceived').addEventListener('input',()=>{let due=totals({items:getItems(),shippingCost:$('shippingCost').value,shippingCharge:$('shippingCharge').value}).due,v=Number($('amountReceived').value||0);$('status').value=v===0?'بانتظار الدفع':v>=due?'تم استلام المبلغ بالكامل':'تم استلام جزء من المبلغ';});")
s=s.replace("$('overdueDays').value=settings.overdueDays;", "const overdue=$('overdueDays');if(overdue)overdue.value=settings.overdueDays;")

logic=r'''
function successCurrency(c){return ({SAR:'🇸🇦 SAR',USD:'🇺🇸 USD',YER:'🇾🇪 YER'})[c]||c||'';}
function successNumber(v){return new Intl.NumberFormat('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}).format(Number(v||0));}
function showSavedOrderSummary(o){const t=totals(o),received=Number(o.amountReceived||0),remaining=Math.max(0,t.due-received),safe=v=>esc(String(v??''));document.getElementById('saveSuccessOverlay')?.remove();const overlay=document.createElement('div');overlay.id='saveSuccessOverlay';overlay.innerHTML=`<section id="saveSuccessCard" role="dialog" aria-modal="true"><button class="ss-x" id="closeSavedX" aria-label="إغلاق">×</button><div class="ss-head"><h3>تم حفظ الطلب بنجاح</h3><div class="ss-check">✓</div></div><div class="ss-meta"><div><small>رقم الطلب:</small><b>${safe(o.id)}</b></div><div><small>اسم العميل:</small><b>${safe(o.customerName)}</b></div><div><small>عدد الأصناف:</small><b>${(o.items||[]).length} أصناف</b></div></div><div class="ss-money"><div class="ss-title">ملخص المبالغ</div><div class="ss-row"><span>إجمالي تكلفة البضاعة:</span><strong class="ss-num">${successNumber(t.cost)}</strong></div><div class="ss-row ss-sale"><span>إجمالي بيع البضاعة:</span><strong class="ss-num">${successNumber(t.sale)}</strong></div><div class="ss-row"><span>الشحن الفعلي:</span><strong class="ss-num">${successNumber(t.sc)}</strong></div><div class="ss-row"><span>الشحن على العميل:</span><strong class="ss-num">${successNumber(t.sh)}</strong></div><div class="ss-row ss-due"><b>المطلوب من العميل:</b><strong class="ss-num">${successNumber(t.due)}</strong></div><div class="ss-row ss-received"><span>المبلغ المستلم:</span><strong class="ss-num">${successNumber(received)}</strong></div><div class="ss-row ss-remaining"><span>المبلغ المتبقي:</span><strong class="ss-num">${successNumber(remaining)}</strong></div></div><div class="ss-currency"><span>العملة:</span><strong>${successCurrency(o.currency)}</strong></div><button type="button" class="ss-close" id="closeSavedOrderSummary">✓　حسناً</button></section>`;document.body.appendChild(overlay);const close=()=>overlay.remove();overlay.querySelector('#closeSavedOrderSummary').onclick=close;overlay.querySelector('#closeSavedX').onclick=close;overlay.addEventListener('click',e=>{if(e.target===overlay)close();});}
'''
s=re.sub(r"function successCurrency\(code\).*?(?=\n(?:function applyDeviceNumberLocale|$))","",s,flags=re.S)
s += "\n"+logic+"\n"
hp.write_text(h,encoding="utf-8"); jp.write_text(s,encoding="utf-8")
print("Applied reference-matched payment, save dialog, and null-safe startup fixes")
