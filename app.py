import streamlit as st
import asyncio
import httpx
from holehe import core
import pandas as pd

# دیزاینی وێبسایتەکە
st.set_page_config(page_title="Cyber AI - Email Finder", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_usage=True)

st.title("🔍 Email OSINT Identifier")
st.write("ئەم ئامرازە بەکاردێت بۆ دۆزینەوەی ناسنامە لە ڕێگەی ئیمەیڵەوە")

email = st.text_input("ئیمەیڵی ئامانج لێرە بنووسە:", placeholder="example@gmail.com")

async def scan_email(target_email):
    results_found = []
    modules = core.import_submodules("holehe.modules")
    tasks = [core.call_module(module, target_email, []) for module in modules]
    
    # پشکنینی Holehe
    responses = await asyncio.gather(*tasks)
    for res in responses:
        if res and res.get("exists"):
            results_found.append({"پلاتفۆرم": res.get("name"), "دۆخ": "✅ ئەکاونت هەیە"})
    return results_found

if st.button("گەڕان دەستپێبکە"):
    if "@" in email:
        with st.spinner('خەریکی پشکنینی داتابەیسەکانم...'):
            try:
                # بەکارهێنانی loop بۆ asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                data = loop.run_until_complete(scan_email(email))
                
                if data:
                    st.success(f"کۆتایی هات! {len(data)} ئەکاونت دۆزرایەوە.")
                    st.table(pd.DataFrame(data))
                    
                    # بەشی دۆزینەوەی یوزەرنەیم
                    user = email.split('@')[0]
                    st.info(f"یوزەرنەیمی پێشبینیکراو: {user}")
                    st.markdown(f"**[🌐 گەڕانی قووڵ لە گوگڵ بۆ ئەم ناسنامەیە](https://www.google.com/search?q=%22{user}%22)**")
                else:
                    st.warning("هیچ ئەکاونتێک لە داتابەیسەکان نەدۆزرایەوە.")
            except Exception as e:
                st.error(f"هەڵەیەک ڕوویدا: {e}")
    else:
        st.error("تکایە ئیمەیڵێکی دروست بنووسە.")
