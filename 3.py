import streamlit as st  # 建议使用 as st 别名
from PIL import Image
import os
from openai import OpenAI
import random

d = "https://www.helloimg.com/i/2026/01/12/6964bf3b9c378.jpg"
c = "https://www.helloimg.com/i/2026/01/12/6964bf3bc3d03.jpg"
f = "https://www.helloimg.com/i/2026/01/12/6964bf3bc5482.jpeg"
h = "https://www.helloimg.com/i/2026/01/12/6964bf3bd9d16.jpg"
e = "https://www.helloimg.com/i/2026/01/12/6964bf3cc89bb.jpg"
j = "https://www.helloimg.com/i/2026/01/12/6964bf3c4bb56.jpg"
k = [d, c, f, h, e, j]

# 删除这行，避免变量名冲突：a=0

st.snow()
st.header(":rainbow[我是哈利波特]")
st.header(":rainbow[请问有什么可以帮助你的吗？]:smile:", divider="rainbow")

a1, a2 = st.columns(2)
with a1:
    # 直接显示图片，不要赋值给变量
    selected_image1 = random.choice(k)
    st.image(selected_image1, width=300)  # 只调用一次

with a2:
    # 同理
    selected_image2 = random.choice(k)
    st.image(selected_image2, width=300)  # 只调用一次

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.sidebar.button('清空历史对话'):
    st.session_state.messages = []
    st.rerun()

st.sidebar.text_area("安全提示：", value="请输入合理合法的问题", label_visibility="visible")
abc = st.sidebar.button("背景", type="primary", use_container_width=False)
if abc:
    st.snow()

chat = st.chat_input("你好")
if chat:
    with st.chat_message("user"):
        st.markdown(chat)
    st.session_state.messages.append({"role": "user", "content": chat})
    
    client = OpenAI(
        api_key='sk-caa08ff7e9c64786b45e9b98ec281ee1',
        base_url="https://api.deepseek.com"
    )
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": chat},
        ],
        stream=False
    )
    
    with st.chat_message("assistant"):
        st.markdown(response.choices[0].message.content)
    
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

# 登录部分
y = 0
x = st.sidebar.text_input("账号", type="default", label_visibility="visible")
if x == "SRH":
    y += 1

t = st.sidebar.text_input("密码", type="password", label_visibility="visible")
if t == "12345678987654321010203040506070809080706050403020101357924681012345678912345678913579246810":
    y += 1

# 这里变量名冲突了，你用了 a，前面也有 a，建议改名
quick_pwd = st.sidebar.text_input("快捷密码", type="password", label_visibility="visible")
if quick_pwd == "847012Dxl":
    y += 1

result = st.sidebar.button("登录", type="primary", use_container_width=False)

if y == 2 or y == 3:
    st.sidebar.markdown('密码正确')
else:
    st.sidebar.markdown('密码错误')
    y = 0  # 这里应该是赋值，不是比较

st.sidebar.markdown('导航：')
st.sidebar.link_button("DeepSeek", "https://www.deepseek.com/")
st.sidebar.link_button("百度", "https://www.baidu.com/")

pinlun = st.sidebar.radio(
    "你觉的这些回答有用吗",
    ["有用", "一般", "没用"],
    captions=["值得鼓励", "继续努力", "需要提升"]
)
st.sidebar.write(f"您觉得{pinlun}")
