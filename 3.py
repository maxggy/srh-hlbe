import streamlit as st
from PIL import Image
import os
from openai import OpenAI
import random

# 图片URL列表
d = "https://www.helloimg.com/i/2026/01/12/6964bf3b9c378.jpg"
c = "https://www.helloimg.com/i/2026/01/12/6964bf3bc3d03.jpg"
f = "https://www.helloimg.com/i/2026/01/12/6964bf3bc5482.jpeg"
h = "https://www.helloimg.com/i/2026/01/12/6964bf3bd9d16.jpg"
e = "https://www.helloimg.com/i/2026/01/12/6964bf3cc89bb.jpg"
j = "https://www.helloimg.com/i/2026/01/12/6964bf3c4bb56.jpg"
k = [d, c, f, h, e, j]

# 页面初始化
st.snow()
st.header(":rainbow[我是哈利波特]")
st.header(":rainbow[请问有什么可以帮助你的吗？]:smile:", divider="rainbow")

# 修改这里：确保两张图片不同
a1, a2 = st.columns(2)

if len(k) >= 2:
    # 方案1：使用random.sample确保两张不同
    selected_images = random.sample(k, 2)
    
    with a1:
        st.image(selected_images[0], width=300)
    
    with a2:
        st.image(selected_images[1], width=300)
else:
    st.warning("图片数量不足")

# 初始化消息历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 侧边栏功能
if st.sidebar.button('清空历史对话'):
    st.session_state.messages = []
    st.rerun()

st.sidebar.text_area("安全提示：", value="请输入合理合法的问题", label_visibility="visible")
abc = st.sidebar.button("背景", type="primary", use_container_width=False)
if abc:
    st.snow()

# 登录部分
y = 0
x = st.sidebar.text_input("账号", type="default", label_visibility="visible")
if x == "SRH":
    y += 1

t = st.sidebar.text_input("密码", type="password", label_visibility="visible")
if t == "12345678987654321010203040506070809080706050403020101357924681012345678912345678913579246810":
    y += 1

quick_pwd = st.sidebar.text_input("快捷密码", type="password", label_visibility="visible")
if quick_pwd == "847012Dxl":
    y += 1

result = st.sidebar.button("登录", type="primary", use_container_width=False)

if y == 2 or y == 3:
    st.sidebar.markdown('密码正确')
else:
    st.sidebar.markdown('密码错误')
    y = 0

st.sidebar.markdown('导航：')
st.sidebar.link_button("DeepSeek", "https://www.deepseek.com/")
st.sidebar.link_button("百度", "https://www.baidu.com/")

pinlun = st.sidebar.radio(
    "你觉得这些回答有用吗",
    ["有用", "一般", "没用"],
    captions=["值得鼓励", "继续努力", "需要提升"]
)
st.sidebar.write(f"您觉得: {pinlun}")

# 聊天输入
chat = st.chat_input("你好")
if chat:
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(chat)
    
    # 保存用户消息到历史
    st.session_state.messages.append({"role": "user", "content": chat})
    
    # 创建OpenAI客户端
    client = OpenAI(
        api_key='sk-caa08ff7e9c64786b45e9b98ec281ee1',
        base_url="https://api.deepseek.com"
    )
    
    # 构建消息列表（包含历史对话）
    messages_for_api = [
        {"role": "system", "content": "You are a helpful assistant"}
    ]
    
    # 添加历史消息
    for msg in st.session_state.messages:
        messages_for_api.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    # 流式调用API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # 调用流式API
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages_for_api,
                stream=True  # 开启流式输出
            )
            
            # 处理流式响应
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    
                    # 实时更新显示（添加光标效果）
                    message_placeholder.markdown(full_response + "▌")
            
            # 最终显示完整回复（去掉光标）
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"调用API时出错: {str(e)}")
            full_response = "抱歉，我暂时无法处理您的请求。"
            message_placeholder.markdown(full_response)
    
    # 保存助手消息到历史
    st.session_state.messages.append({"role": "assistant", "content": full_response})
