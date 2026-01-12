import streamlit as st
from PIL import Image
import os
import random
from cozepy import Coze, TokenAuth, Message, ChatEventType, COZE_CN_BASE_URL

# 定义图片URL列表
d = "https://www.helloimg.com/i/2026/01/12/6964bf3b9c378.jpg"
c = "https://www.helloimg.com/i/2026/01/12/6964bf3bc3d03.jpg"
f = "https://www.helloimg.com/i/2026/01/12/6964bf3bc5482.jpeg"
h = "https://www.helloimg.com/i/2026/01/12/6964bf3bd9d16.jpg"
e = "https://www.helloimg.com/i/2026/01/12/6964bf3cc89bb.jpg"
j = "https://www.helloimg.com/i/2026/01/12/6964bf3c4bb56.jpg"

# 图片列表
b = [c, d, e, f, h, j]

# 初始化Coze
coze_api_token = 'pat_kINCEUMRBdvFInNFswdz4nPYhfnhqaR6AY1rtCOQxkOtrJM0vuM5JVmUH9Nb0UiD'
bot_id = '7567584264184053775'
user_id = '123456789'
coze = Coze(
    auth=TokenAuth(token=coze_api_token),
    base_url=COZE_CN_BASE_URL
)

# 页面初始化
st.snow()
st.header(":rainbow[我是哈利波特]")
st.header(":rainbow[请问有什么可以帮助你的吗？]:smile:", divider="rainbow")

# 修改这里：确保两张图片不同
a1, a2 = st.columns(2)

if len(b) >= 2:
    # 确保选择两张不同的图片
    selected_images = random.sample(b, 2)
    
    with a1:
        st.image(selected_images[0], width=100)
    
    with a2:
        st.image(selected_images[1], width=100)
else:
    st.warning("图片数量不足，无法显示两张不同的图片")

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

# 登录系统
y = 0  # 登录验证计数器
x = st.sidebar.text_input("账号", type="default", label_visibility="visible")
if x == "SRH":
    y += 1

t = st.sidebar.text_input("密码", type="password", label_visibility="visible")
if t == "12345678987654321010203040506070809080706050403020101357924681012345678912345678913579246810":
    y += 1

# 使用不同的变量名，避免与前面的变量冲突
quick_pwd = st.sidebar.text_input("快捷密码", type="password", label_visibility="visible")
if quick_pwd == "847012Dxl":
    y += 1

result = st.sidebar.button("登录", type="primary", use_container_width=False)

if y == 2 or y == 3:
    st.sidebar.markdown('密码正确')
else:
    st.sidebar.markdown('密码错误')
    y = 0  # 修正：应该是赋值，不是比较

st.sidebar.markdown('导航：')
st.sidebar.link_button("DeepSeek", "https://www.deepseek.com/")
st.sidebar.link_button("百度", "https://www.baidu.com/")

pinlun = st.sidebar.radio(
    "你觉得这些回答有用吗",
    ["有用", "一般", "没用"],
    captions=["值得鼓励", "继续努力", "需要提升"]
)
st.sidebar.write(f"您觉得: {pinlun}")

# 聊天输入（应该放在最后）
chat = st.chat_input("你好")

if chat:
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(chat)
    
    # 保存用户消息到历史
    st.session_state.messages.append({"role": "user", "content": chat})
    
    # 准备消息历史给Coze
    # 注意：这里有一个潜在问题，我们构建additional_messages时只包含用户消息
    # 实际上，对话应该包含用户和助手的历史消息
    # 根据Coze文档，我们需要构建完整的对话历史
    
    # 构建完整的对话历史
    additional_messages = []
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            additional_messages.append(Message.build_user_question_text(msg["content"]))
        elif msg["role"] == "assistant":
            additional_messages.append(Message.build_assistant_answer_text(msg["content"]))
    
    # 调用Coze API并显示流式响应
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # 调用Coze API
            for event in coze.chat.stream(
                bot_id=bot_id,
                user_id=user_id,
                additional_messages=additional_messages,
            ):
                if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                    if event.message.content:
                        full_response += event.message.content
                        message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # 保存助手消息到历史
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        except Exception as e:
            st.error(f"调用Coze API时出错: {str(e)}")
