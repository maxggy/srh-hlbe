import streamlit as st  # 使用别名 st
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
# 注意：这里没有g，所以只包含已有的变量
b = [c, d, e, f, h, j]  # 移除了不存在的g

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

# 显示图片
a1, a2 = st.columns(2)  # 修正拼写：stramlit -> st
with a1:
    selected_image1 = random.choice(b)
    st.image(selected_image1, width=300)
with a2:
    selected_image2 = random.choice(b)
    st.image(selected_image2, width=300)

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
    "你觉的这些回答有用吗",
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
    additional_messages = []
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            additional_messages.append(Message.build_user_question_text(msg["content"]))
    
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
                    full_response += event.message.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # 保存助手消息到历史
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        except Exception as e:
            st.error(f"调用Coze API时出错: {str(e)}")

