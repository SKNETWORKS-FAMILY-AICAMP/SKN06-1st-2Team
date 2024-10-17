import streamlit as st
import pandas as pd

# 데이터프레임을 사용하여 게시물과 댓글 저장
if 'posts' not in st.session_state:
    st.session_state.posts = []

if 'comments' not in st.session_state:
    st.session_state.comments = {}

# 게시물 작성
def create_post():
    nickname = st.text_input("닉네임을 입력하세요:")
    post_content = st.text_area("게시물 내용을 입력하세요:")
    
    if st.button("게시물 작성"):
        if nickname and post_content:
            post = {"nickname": nickname, "content": post_content}
            st.session_state.posts.append(post)
            st.success("게시물이 작성되었습니다!")
        else:
            st.error("닉네임과 게시물 내용을 입력하세요.")

# 댓글 달기
def add_comment(post_index):
    nickname = st.text_input("닉네임을 입력하세요:", key=f"nickname_{post_index}")
    comment_content = st.text_area("댓글 내용을 입력하세요:", key=f"comment_{post_index}")
    
    if st.button("댓글 달기", key=f"comment_button_{post_index}"):
        if nickname and comment_content:
            if post_index not in st.session_state.comments:
                st.session_state.comments[post_index] = []
            st.session_state.comments[post_index].append({"nickname": nickname, "content": comment_content})
            st.success("댓글이 작성되었습니다!")
        else:
            st.error("닉네임과 댓글 내용을 입력하세요.")

# 게시물 표시 및 댓글 기능
def display_posts():
    for index, post in enumerate(st.session_state.posts):
        st.subheader(f"게시물 {index + 1}")
        st.write(f"**닉네임:** {post['nickname']}")
        st.write(f"**내용:** {post['content']}")
        
        # 댓글 표시
        if index in st.session_state.comments:
            for comment in st.session_state.comments[index]:
                st.write(f"**{comment['nickname']}:** {comment['content']}")
        
        # 댓글 추가 UI
        add_comment(index)
        st.markdown("---")

# 앱 UI
st.title("게시물 작성 및 댓글 기능")
create_post()
st.markdown("---")
display_posts()
