import streamlit
from PIL import Image
import os
from openai import OpenAI
import random
d="https://www.helloimg.com/i/2026/01/12/6964bf3b9c378.jpg"
c="https://www.helloimg.com/i/2026/01/12/6964bf3bc3d03.jpg"
f="https://www.helloimg.com/i/2026/01/12/6964bf3bc5482.jpeg"
h="https://www.helloimg.com/i/2026/01/12/6964bf3bd9d16.jpg"
e="https://www.helloimg.com/i/2026/01/12/6964bf3cc89bb.jpg"
j="https://www.helloimg.com/i/2026/01/12/6964bf3c4bb56.jpg"
k=[d,c,f,h,e,j]
a=0
streamlit.snow()
streamlit.header(":rainbow[我是哈利波特]")
streamlit.header(":rainbow[请问有什么可以帮助你的吗？]:smile:",divider="rainbow")
a1,a2=streamlit.columns(2)
with a1:
    image1=st.image(random.choice(k))
    streamlit.image(image1,width=300)
with a2:
    image2=st.image(random.choice(k))
    streamlit.image(image2,width=300)
if "messages" not in streamlit.session_state:
    streamlit.session_state.messages = []
for message in streamlit.session_state.messages:
    with streamlit.chat_message(message["role"]):
        streamlit.markdown(message["content"]) 
if streamlit.sidebar.button('清空历史对话'):
    streamlit.session_state.messages = []
    streamlit.rerun()
streamlit.sidebar.text_area("安全提示：",value="请输入合理合法的问题",label_visibility="visible")
abc = streamlit.sidebar.button("背景",type="primary",use_container_width=False)
if abc:
    streamlit.snow()
chat = streamlit.chat_input("你好")
if chat:
    with streamlit.chat_message("user"):
        streamlit.markdown(chat)
    streamlit.session_state.messages.append({"role":"user","content":chat})
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
    streamlit.markdown(response.choices[0].message.content)
    streamlit.session_state.messages.append({"role":"assistant","content":response.choices[0].message.content})
y=0
x=streamlit.sidebar.text_input("账号",type="default",label_visibility="visible")
if x=="SRH":
    y+=1
t=streamlit.sidebar.text_input("密码",type="password",label_visibility="visible")
if t=="12345678987654321010203040506070809080706050403020101357924681012345678912345678913579246810":
    y+=1
a=streamlit.sidebar.text_input("快捷密码",type="password",label_visibility="visible")
if a=="847012Dxl":
    y+=1
result = streamlit.sidebar.button("登录",type="primary",use_container_width=False)

if y==2 or y==3:
    streamlit.sidebar.markdown('密码正确')
else:
    streamlit.sidebar.markdown('密码错误')
    y==0
streamlit.sidebar.markdown('导航：')
streamlit.sidebar.link_button("DeepSeek","https://www.deepseek.com/")
streamlit.sidebar.link_button("百度","https://www.baidu.com/")
pinlun = streamlit.sidebar.radio("你觉的这些回答有用吗",["有用","一般","没用"],captions=["值得鼓励","继续努力","需要提升"])
streamlit.sidebar.write("您觉得",pinlun)
    


