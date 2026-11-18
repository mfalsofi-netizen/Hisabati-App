from pathlib import Path
import re
app=next(Path("appsrc").rglob("package.json")).parent
hp=app/"www"/"index.html"; jp=app/"www"/"app.js"
h=hp.read_text(encoding="utf-8"); s=jp.read_text(encoding="utf-8")
h=h.replace('<option value="SAR">ريال سعودي (SAR)</option><option value="USD">دولار أمريكي (USD)</option>','<option value="SAR">🇸🇦 ريال سعودي (SAR)</option><option value="USD">🇺🇸 دولار أمريكي (USD)</option><option value="YER">🇾🇪 ريال يمني (YER)</option>')
h=h.replace('<option value="SAR">SAR</option><option value="USD">USD</option>','<option value="SAR">🇸🇦 SAR</option><option value="USD">🇺🇸 USD</option><option value="YER">🇾🇪 YER</option>')
h=h.replace('تكلفة الشحن عليك','تكلفة الشحن الفعلية').replace('تكلفة الشحن المطلوب من العميل','تكلفة الشحن على العميل')
h=h.replace('مراجعة الطلبية قبل الحفظ','💾 حفظ الطلب').replace('تفريغ الحقول','↩ إلغاء الطلب').replace('استيراد من دليل الهاتف','📇 دليل الهاتف')
h=h.replace('<span>سعر بيع الوحدة</span><span></span>','<span>سعر بيع الوحدة</span><span>الإجمالي</span><span></span>')
h=h.replace('id="receivedAmountWrap" class="hidden"','id="receivedAmountWrap"').replace('كل الحالات','كل حالات الدفع')
h=h.replace('</style></head>','input[type=number]{direction:ltr;text-align:left;font-variant-numeric:tabular-nums}.payment-status[data-state=pending]{color:#b42318;background:#fff1f0}.payment-status[data-state=partial]{color:#a15c00;background:#fff7e6}.payment-status[data-state=paid]{color:#16834b;background:#edfff4}.order-summary{background:#fff8c9!important;border-color:#ecd875!important}.sum-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}.sum-item{background:#fffdf0;border:1px solid #f0e3a5;border-radius:9px;padding:9px}.sum-item small{display:block;font-size:11px;margin-bottom:4px}.sum-item b{display:block;font-size:15px;direction:ltr}.sum-cost b{color:#475569}.sum-sale b{color:#1769aa}.sum-due b{color:#b45309}.sum-profit b{color:#16834b}.itemline{grid-template-columns:minmax(100px,2fr) 42px 65px 65px 70px 26px!important;min-width:380px!important;gap:4px!important}.lineTotal{font-size:11px;text-align:center;direction:ltr;white-space:nowrap;font-weight:bold;color:#1769aa}</style></head>')
h=h.replace('id="orderSummary" class="notice"','id="orderSummary" class="notice order-summary"')
pm=re.search(r'<div class="row"><div><label>حالة الدفع</label>.*?</div></div>',h,re.S)
if pm:
 block=pm.group(0);h=h[:pm.start()]+h[pm.end():]
 sh=re.search(r'<div class="row"><div><label>تكلفة الشحن الفعلية</label>.*?</div></div>',h,re.S)
 if sh:h=h[:sh.end()]+block+h[sh.end():]
h=re.sub(r'<div><label>حالة تنفيذ الطلب</label>.*?</div>','',h,flags=re.S)
hp.write_text(h,encoding="utf-8")
s=re.sub(r'function addItemRow\(.*?\nfunction getItems\(\)',"""function addItemRow(item={name:'',qty:'',cost:'',price:''}){
 let d=document.createElement('div');d.className='itemline';
 d.innerHTML='<input class="iname" placeholder="اسم الصنف" value="'+esc(item.name)+'"><input class="iqty" type="number" min="1" step="1" lang="en" placeholder="—" value="'+(item.qty??'')+'"><input class="icost" type="number" min="0" step=".01" lang="en" placeholder="—" value="'+(item.cost??'')+'"><input class="iprice" type="number" min="0" step=".01" lang="en" placeholder="—" value="'+(item.price??'')+'"><span class="lineTotal">0.00</span><button class="btn red delItem" type="button">×</button>';
 $('items').append(d);d.querySelectorAll('input').forEach(x=>{x.lang='en';x.addEventListener('input',()=>{updateLineTotal(d);calcSummary();syncFullPayment();});});
 d.querySelector('.delItem').onclick=()=>{d.remove();calcSummary();syncFullPayment();};updateLineTotal(d);calcSummary();
}
function updateLineTotal(r){let q=Number(r.querySelector('.iqty').value||0),p=Number(r.querySelector('.iprice').value||0);r.querySelector('.lineTotal').textContent=(q*p).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function getItems()""",s,count=1,flags=re.S)
s=re.sub(r'function calcSummary\(\)\{.*?\n',"""function calcSummary(){let o={items:getItems(),shippingCost:$('shippingCost').value,shippingCharge:$('shippingCharge').value,currency:$('currency').value},t=totals(o);$('orderSummary').innerHTML='<div class="sum-grid"><div class="sum-item sum-cost"><small>إجمالي تكلفة البضاعة</small><b>'+money(t.cost,o.currency)+'</b></div><div class="sum-item sum-sale"><small>إجمالي بيع البضاعة</small><b>'+money(t.sale,o.currency)+'</b></div><div class="sum-item sum-due"><small>إجمالي المطلوب من العميل</small><b>'+money(t.due,o.currency)+'</b></div><div class="sum-item sum-profit"><small>صافي الربح من الطلب</small><b>'+money(t.profit,o.currency)+'</b></div></div>';}
""",s,count=1,flags=re.S)
s=re.sub(r'function formData\(\)\{.*?\nfunction validate\(o\)\{.*?\n\}',"""function formData(){let items=getItems();return {id:$('editId').value||('ORD-'+Date.now()),date:today(),customerName:$('customerName').value.trim(),customerPhone:$('customerPhone').value.trim(),currency:$('currency').value,paymentStatus:$('paymentStatus').value,amountReceived:Number($('amountReceived').value||0),items,shippingCost:Number($('shippingCost').value||0),shippingCharge:Number($('shippingCharge').value||0),notes:$('orderNotes').value};}
function validate(o){if(!o.customerName)return 'أدخل اسم العميل';if(!o.items.length)return 'أضف صنفاً واحداً على الأقل';for(let x of o.items){if(!x.name||!(x.qty>0)||x.cost<0||x.price<0)return 'تحقق من بيانات الأصناف';if(x.price<x.cost)return 'سعر بيع الوحدة لا يمكن أن يكون أقل من تكلفة الوحدة';}if(o.shippingCost<0||o.shippingCharge<0)return 'قيمة الشحن لا يمكن أن تكون سالبة';let due=totals(o).due;if(o.paymentStatus==='بانتظار الدفع'&&o.amountReceived!==0)return 'المبلغ المستلم يجب أن يساوي صفراً عند انتظار الدفع';if(o.paymentStatus==='تم استلام جزء من المبلغ'&&!(o.amountReceived>0&&o.amountReceived<=due))return 'المبلغ المستلم يجب أن يكون أكبر من صفر وأقل من أو يساوي المبلغ المطلوب';if(o.paymentStatus==='تم استلام المبلغ بالكامل'&&Math.abs(o.amountReceived-due)>.001)return 'المبلغ المستلم يجب أن يساوي إجمالي المطلوب من العميل';return '';}""",s,count=1,flags=re.S)
payment="""function syncFullPayment(){if($('paymentStatus').value==='تم استلام المبلغ بالكامل'){let o={items:getItems(),shippingCharge:$('shippingCharge').value,currency:$('currency').value};$('amountReceived').value=totals(o).due.toFixed(2);}}
function updatePaymentFields(){let st=$('paymentStatus').value,a=$('amountReceived');$('receivedAmountWrap').classList.remove('hidden');$('paymentStatus').dataset.state=st==='بانتظار الدفع'?'pending':st==='تم استلام جزء من المبلغ'?'partial':'paid';a.readOnly=st!=='تم استلام جزء من المبلغ';if(st==='بانتظار الدفع')a.value='0';if(st==='تم استلام المبلغ بالكامل')syncFullPayment();}
$('paymentStatus').addEventListener('change',updatePaymentFields);$('shippingCharge').addEventListener('input',()=>{calcSummary();syncFullPayment();});$('currency').addEventListener('change',()=>{calcSummary();syncFullPayment();});$('amountReceived').lang='en';
"""
if "function syncFullPayment()" not in s:s=s.replace("function formData()",payment+"function formData()")
s=re.sub(r'function clearForm\(\)\{.*?\n\}',"""function clearForm(){$('editId').value='';$('formTitle').textContent='طلب جديد';['customerName','customerPhone','orderNotes','shippingCost','shippingCharge'].forEach(x=>$(x).value='');$('currency').value='SAR';$('paymentStatus').value='بانتظار الدفع';$('amountReceived').value='0';$('items').innerHTML='';addItemRow();updatePaymentFields();calcSummary();}""",s,count=1,flags=re.S)
s=re.sub(r'function editOrder\(id\)\{.*?\n\}',"""function editOrder(id){let o=orders.find(x=>x.id===id);if(!o)return;showPage('new');$('editId').value=o.id;$('formTitle').textContent='تعديل الطلب';$('customerName').value=o.customerName;$('customerPhone').value=o.customerPhone;$('currency').value=o.currency||'SAR';$('paymentStatus').value=o.paymentStatus||'بانتظار الدفع';$('shippingCost').value=o.shippingCost??'';$('shippingCharge').value=o.shippingCharge??'';$('orderNotes').value=o.notes||'';$('items').innerHTML='';o.items.forEach(addItemRow);$('amountReceived').value=o.amountReceived??0;updatePaymentFields();calcSummary();}""",s,count=1,flags=re.S)
s=re.sub(r'function orderCard\(o\)\{.*?\nwindow\.editOrder=editOrder;',"""function orderCard(o){let t=totals(o),ps=o.paymentStatus||'بانتظار الدفع';return '<div class="panel"><div class="row"><div><b>'+esc(o.customerName)+'</b><div class="muted">'+esc(o.id)+' · '+o.date+' · '+esc(o.customerPhone)+'</div></div><div><span class="pill">'+esc(ps)+'</span><div><b>'+money(t.due,o.currency)+'</b></div><div class="muted">المستلم: '+money(o.amountReceived||0,o.currency)+' — المتبقي: '+money(Math.max(0,t.due-(o.amountReceived||0)),o.currency)+'</div></div></div><div class="muted">صافي الربح: '+money(t.profit,o.currency)+'</div><div class="actions"><button class="btn light" onclick="editOrder(\\''+o.id+'\\')">تعديل</button><button class="btn red" onclick="deleteOrder(\\''+o.id+'\\')">حذف</button><button class="btn light" onclick="printInvoice(\\''+o.id+'\\')">طباعة الفاتورة</button></div></div>';}
window.editOrder=editOrder;""",s,count=1,flags=re.S)
s=re.sub(r'function renderOrders\(\)\{.*?\n\}',"""function renderOrders(){let q=($('orderSearch')?.value||'').toLowerCase(),st=$('filterStatus')?.value||'',cu=$('filterCurrency')?.value||'';let arr=orders.filter(o=>(!q||[o.id,o.customerName,o.customerPhone].join(' ').toLowerCase().includes(q))&&(!st||(o.paymentStatus||'بانتظار الدفع')===st)&&(!cu||o.currency===cu));$('ordersList').innerHTML=arr.length?arr.map(orderCard).join(''):'<p class="muted">لا توجد طلبات مطابقة.</p>';}
""",s,count=1,flags=re.S)
s=s.replace("for(let c of ['SAR','USD'])","for(let c of ['SAR','USD','YER'])").replace("['SAR','USD'].map(c=>","['SAR','USD','YER'].map(c=>")
s=s.replace("a.filter(x=>x.status==='بانتظار الدفع').length","a.filter(x=>(x.paymentStatus||'بانتظار الدفع')==='بانتظار الدفع').length").replace("a.filter(x=>x.status!=='بانتظار الدفع').length","a.filter(x=>(x.paymentStatus||'بانتظار الدفع')!=='بانتظار الدفع').length")
s=s.replace("o.status==='بانتظار الدفع'","(o.paymentStatus||'بانتظار الدفع')==='بانتظار الدفع'")
s=re.sub(r'function printInvoice\(id\)\{.*?\nwindow\.printInvoice=printInvoice;',"""function printInvoice(id){let o=orders.find(x=>x.id===id);if(!o)return;let t=totals(o),received=Number(o.amountReceived||0),remaining=Math.max(0,t.due-received);let rows=o.items.map(x=>'<div class="receipt-item"><b>'+esc(x.name)+'</b><div class="receipt-line"><span>'+x.qty+' × '+money(x.price,o.currency)+'</span><strong>'+money(x.qty*x.price,o.currency)+'</strong></div></div>').join('');let content='<div class="receipt-head"><h2>فاتورة طلب شراء</h2><div>رقم الطلب: '+esc(o.id)+'</div><div>التاريخ: '+esc(o.date)+'</div></div><div class="receipt-customer"><b>العميل:</b> '+esc(o.customerName)+(o.customerPhone?'<br><b>الهاتف:</b> '+esc(o.customerPhone):'')+'</div><div class="receipt-status">'+esc(o.paymentStatus||'بانتظار الدفع')+'</div>'+rows+'<div class="receipt-totals"><div><span>إجمالي البضاعة</span><b>'+money(t.sale,o.currency)+'</b></div><div><span>تكلفة الشحن على العميل</span><b>'+money(t.sh,o.currency)+'</b></div><div class="grand"><span>الإجمالي المطلوب</span><b>'+money(t.due,o.currency)+'</b></div><div><span>المبلغ المستلم</span><b>'+money(received,o.currency)+'</b></div><div><span>المتبقي</span><b>'+money(remaining,o.currency)+'</b></div></div>'+(o.notes?'<div class="receipt-notes">ملاحظات: '+esc(o.notes)+'</div>':'')+'<div class="receipt-thanks">شكراً لتعاملكم معنا</div>';printDocument('فاتورة طلب شراء',content,'80mm');}
window.printInvoice=printInvoice;""",s,count=1,flags=re.S)
h=h.replace('</style></head>','''#printRoot{font-family:Tahoma,Arial,sans-serif}.receipt-head{text-align:center;border-bottom:1px dashed #333;padding-bottom:8px;margin-bottom:8px}.receipt-head h2{font-size:16px;margin:0 0 7px;color:#111}.receipt-head div,.receipt-customer{font-size:10px;line-height:1.8}.receipt-customer{padding:6px 0;border-bottom:1px dashed #777}.receipt-status{text-align:center;font-weight:bold;font-size:12px;padding:7px 2px;border-bottom:1px dashed #777}.receipt-item{padding:6px 0;border-bottom:1px dotted #aaa;font-size:11px;break-inside:avoid}.receipt-line,.receipt-totals>div{display:flex;justify-content:space-between;gap:5px;font-size:10px;line-height:1.8}.receipt-line span{direction:ltr}.receipt-totals{padding-top:7px}.receipt-totals .grand{font-size:12px;font-weight:bold;border-top:1px solid #111;border-bottom:1px solid #111;padding:5px 0;margin:4px 0}.receipt-notes{font-size:10px;margin-top:8px}.receipt-thanks{text-align:center;font-size:11px;font-weight:bold;border-top:1px dashed #777;margin-top:10px;padding-top:9px}@media print{body.printing.print-80mm #printRoot{width:74mm!important;max-width:74mm!important;margin:0 auto!important;padding:0 1mm!important}body.printing.print-80mm #printRoot *{color:#111!important}}</style></head>''')
hp.write_text(h,encoding="utf-8");jp.write_text(s,encoding="utf-8")
print("Final approved changes applied")


# Action icons and WhatsApp invoice sharing (appended after the main patch).
h=hp.read_text(encoding="utf-8")
s=jp.read_text(encoding="utf-8")
s=s.replace('>تعديل</button>','>✏️ تعديل</button>')
s=s.replace('>حذف</button>','>🗑️ حذف</button>')
s=s.replace('>طباعة الفاتورة</button>', """ >🖨️ طباعة الفاتورة</button><button class="btn whatsapp" aria-label="مشاركة الفاتورة عبر واتساب" onclick="shareInvoiceWhatsApp(\\''+o.id+'\\')">🟢 واتساب</button>""")
if "function shareInvoiceWhatsApp(id)" not in s:
 s += r"""
function shareInvoiceWhatsApp(id){
 let o=orders.find(x=>x.id===id);if(!o)return;
 let t=totals(o),lines=o.items.map(x=>'• '+x.name+' — '+x.qty+' × '+money(x.price,o.currency)+' = '+money(x.qty*x.price,o.currency)).join('\n');
 let received=Number(o.amountReceived||0),remaining=Math.max(0,t.due-received);
 let message='فاتورة طلب شراء\nرقم الطلب: '+o.id+'\nالتاريخ: '+o.date+'\nالعميل: '+o.customerName+(o.customerPhone?'\nالهاتف: '+o.customerPhone:'')+'\n\n'+lines+'\n\nإجمالي البضاعة: '+money(t.sale,o.currency)+'\nتكلفة الشحن على العميل: '+money(t.sh,o.currency)+'\nالإجمالي المطلوب: '+money(t.due,o.currency)+'\nالمبلغ المستلم: '+money(received,o.currency)+'\nالمتبقي: '+money(remaining,o.currency)+'\nحالة الدفع: '+(o.paymentStatus||'بانتظار الدفع');
 window.open('https://wa.me/?text='+encodeURIComponent(message),'_blank');
}
window.shareInvoiceWhatsApp=shareInvoiceWhatsApp;
"""
h=h.replace('</style></head>',' .btn.whatsapp{background:#168b4b!important;color:#fff!important;border-color:#168b4b!important}</style></head>')

# Restore core order, dashboard, customer and save handlers omitted by an earlier patch.
s=s.replace("if(page==='new'&&!$('editId').value)addItemRow();","if(page==='new'&&!$('editId').value&&$('items').children.length===0)addItemRow();")
s += r"""
function paymentState(o){return o.paymentStatus||o.status||'بانتظار الدفع';}
function orderCard(o){
 const t=totals(o),st=paymentState(o);
 return '<div class="panel order-card"><div class="row"><div><b>'+esc(o.customerName)+'</b><div class="muted">'+esc(o.id)+' · '+esc(o.date||'')+'</div><div class="muted">'+esc(o.customerPhone||'')+'</div></div><div><b>'+money(t.due,o.currency)+'</b><div class="pill">'+esc(st)+'</div><div class="muted">المتبقي: '+money(Math.max(0,t.due-Number(o.amountReceived||0)),o.currency)+'</div></div></div><div class="actions"><button class="btn light" data-action="edit" data-id="'+esc(o.id)+'">✏️ تعديل</button><button class="btn red" data-action="delete" data-id="'+esc(o.id)+'">🗑️ حذف</button><button class="btn light" data-action="print" data-id="'+esc(o.id)+'">🖨️ طباعة الفاتورة</button><button class="btn whatsapp" data-action="whatsapp" data-id="'+esc(o.id)+'">🟢 واتساب</button></div></div>';
}
function renderOrders(){
 const q=($('orderSearch').value||'').trim().toLowerCase(),st=$('filterStatus').value,cu=$('filterCurrency').value;
 const arr=orders.filter(o=>(!q||[o.id,o.customerName,o.customerPhone].join(' ').toLowerCase().includes(q))&&(!st||paymentState(o)===st)&&(!cu||o.currency===cu)).sort((a,b)=>(b.date||'').localeCompare(a.date||''));
 $('ordersList').innerHTML=arr.length?arr.map(orderCard).join(''):'<p class="muted">لا توجد طلبات مطابقة.</p>';
}
function renderDashboard(){
 const currencies=['SAR','USD','YER'];
 $('dashboardStats').innerHTML=currencies.map(c=>{const a=orders.filter(o=>o.currency===c),due=a.reduce((v,o)=>v+totals(o).due,0),profit=a.reduce((v,o)=>v+totals(o).profit,0),pending=a.filter(o=>paymentState(o)==='بانتظار الدفع').length;return '<div class="panel"><h3>'+c+'</h3><div>عدد الطلبات: <b>'+a.length+'</b></div><div>إجمالي المطلوب: <b>'+money(due,c)+'</b></div><div>صافي الربح: <b>'+money(profit,c)+'</b></div><div>بانتظار الدفع: <b>'+pending+'</b></div></div>';}).join('');
 const recent=[...orders].sort((a,b)=>(b.date||'').localeCompare(a.date||'')).slice(0,5);
 $('recentOrders').innerHTML=recent.length?recent.map(orderCard).join(''):'<p class="muted">لا توجد طلبات حتى الآن.</p>';
}
function renderCustomers(){
 const map=new Map();
 orders.forEach(o=>{const key=(o.customerPhone||o.customerName||'').trim();if(!key)return;let c=map.get(key)||{name:o.customerName,phone:o.customerPhone,orders:[],due:0,received:0};c.orders.push(o);c.due+=totals(o).due;c.received+=Number(o.amountReceived||0);map.set(key,c);});
 $('customersList').innerHTML=[...map.values()].sort((a,b)=>a.name.localeCompare(b.name,'ar')).map(c=>'<div class="panel"><b>'+esc(c.name)+'</b><div class="muted">'+esc(c.phone||'')+' · '+c.orders.length+' طلب</div><div>إجمالي المطلوب: '+money(c.due,c.orders[0].currency)+'</div><div>المستلم: '+money(c.received,c.orders[0].currency)+'</div><div>المتبقي: '+money(Math.max(0,c.due-c.received),c.orders[0].currency)+'</div></div>').join('')||'<p class="muted">لا يوجد زبائن مسجلون.</p>';
}
function clearForm(){
 $('editId').value='';$('formTitle').textContent='طلب جديد';
 ['customerName','customerPhone','orderNotes'].forEach(id=>$(id).value='');
 $('currency').value='SAR';$('shippingCost').value='';$('shippingCharge').value='';
 $('paymentStatus').value='بانتظار الدفع';$('amountReceived').value='0';
 $('items').innerHTML='';addItemRow();updatePaymentFields();calcSummary();
}
function editOrder(id){
 const o=orders.find(x=>x.id===id);if(!o)return;
 $('editId').value=o.id;$('formTitle').textContent='تعديل الطلب';
 $('customerName').value=o.customerName||'';$('customerPhone').value=o.customerPhone||'';
 $('currency').value=o.currency||'SAR';$('shippingCost').value=o.shippingCost??'';
 $('shippingCharge').value=o.shippingCharge??'';$('paymentStatus').value=paymentState(o);
 $('amountReceived').value=Number(o.amountReceived||0);$('orderNotes').value=o.notes||'';
 $('items').innerHTML='';(o.items||[]).forEach(addItemRow);if(!o.items?.length)addItemRow();
 updatePaymentFields();if(paymentState(o)==='تم استلام جزء من المبلغ')$('amountReceived').value=Number(o.amountReceived||0);
 calcSummary();showPage('new');
}
async function deleteOrder(id){
 if(!confirm('هل تريد حذف هذا الطلب نهائياً؟'))return;
 orders=orders.filter(o=>o.id!==id);await saveAll();
}
function showReview(){
 const o=formData(),error=validate(o);if(error){alert(error);return;}
 const t=totals(o),received=Number(o.amountReceived||0);
 $('reviewBody').innerHTML='<p><b>العميل:</b> '+esc(o.customerName)+' — '+esc(o.customerPhone)+'</p><p><b>عدد الأصناف:</b> '+o.items.length+'</p><p><b>إجمالي المطلوب:</b> '+money(t.due,o.currency)+'</p><p><b>المبلغ المستلم:</b> '+money(received,o.currency)+'</p><p><b>المتبقي:</b> '+money(t.due-received,o.currency)+'</p><p><b>حالة الدفع:</b> '+esc(o.paymentStatus)+'</p>';
 $('modal').classList.remove('hidden');
}
async function confirmSaveOrder(){
 const o=formData(),error=validate(o);if(error){alert(error);$('modal').classList.add('hidden');return;}
 const idx=orders.findIndex(x=>x.id===o.id);if(idx>=0)orders[idx]=o;else orders.unshift(o);
 await saveAll();$('modal').classList.add('hidden');clearForm();showPage('orders');
}
$('reviewOrder').addEventListener('click',showReview);
$('confirmSave').addEventListener('click',confirmSaveOrder);
$('backEdit').addEventListener('click',()=>$('modal').classList.add('hidden'));
$('clearForm').addEventListener('click',()=>{if(confirm('إلغاء الإدخال الحالي؟ لن يتم حذف أي طلب محفوظ.'))clearForm();});
$('orderSearch').addEventListener('input',renderOrders);
$('filterStatus').addEventListener('change',renderOrders);
$('filterCurrency').addEventListener('change',renderOrders);
document.addEventListener('click',e=>{
 const b=e.target.closest('[data-action][data-id]');if(!b)return;
 const id=b.dataset.id,action=b.dataset.action;
 if(action==='edit')editOrder(id);
 if(action==='delete')deleteOrder(id);
 if(action==='print')printInvoice(id);
 if(action==='whatsapp')shareInvoiceWhatsApp(id);
});
window.editOrder=editOrder;window.deleteOrder=deleteOrder;
"""
hp.write_text(h,encoding="utf-8")
jp.write_text(s,encoding="utf-8")

hp.write_text(h,encoding="utf-8")
jp.write_text(s,encoding="utf-8")

# Runtime compatibility and visible diagnostics for Android WebView.
h=hp.read_text(encoding="utf-8")
s=jp.read_text(encoding="utf-8")
# This application uses no import/export; a classic script is more compatible with older Android WebViews.
h=h.replace('<script type="module" src="app.js"></script>','''<script>
(function(){
  function showError(message){
    var box=document.getElementById('runtimeError');
    if(!box){box=document.createElement('div');box.id='runtimeError';box.style.cssText='position:fixed;bottom:0;left:0;right:0;z-index:99999;background:#8b1e1e;color:#fff;padding:12px;font:13px Tahoma;direction:rtl;max-height:35vh;overflow:auto';document.body.appendChild(box);}
    box.textContent='حدث خطأ في تشغيل التطبيق: '+message;
  }
  window.addEventListener('error',function(e){showError((e.message||'خطأ غير معروف')+' — '+(e.filename||'')+':'+(e.lineno||''));});
  window.addEventListener('unhandledrejection',function(e){showError(String(e.reason&&e.reason.message||e.reason||'Promise error'));});
  document.addEventListener('DOMContentLoaded',function(){
    var nav=document.getElementById('nav');
    if(nav)nav.addEventListener('click',function(e){
      var b=e.target.closest('button[data-page]');if(!b)return;
      document.querySelectorAll('.page').forEach(function(p){p.classList.toggle('hidden',p.id!==b.dataset.page);});
      document.querySelectorAll('nav button').forEach(function(x){x.classList.toggle('active',x===b);});
    });
  });
})();
</script><script src="app.js"></script>''')
# Guard against old/corrupt local records preventing screens from rendering.
s=s.replace("orders=await get('orders')||[];expenses=await get('expenses')||[];", "orders=await get('orders')||[];expenses=await get('expenses')||[];if(!Array.isArray(orders))orders=[];if(!Array.isArray(expenses))expenses=[];orders=orders.map(o=>({...o,items:Array.isArray(o.items)?o.items:[]}));")
s=s.replace("let cost=o.items.reduce(", "let items=Array.isArray(o.items)?o.items:[];let cost=items.reduce(")
s=s.replace(",sale=o.items.reduce(", ",sale=items.reduce(")
jp.write_text(s,encoding="utf-8")
hp.write_text(h,encoding="utf-8")
