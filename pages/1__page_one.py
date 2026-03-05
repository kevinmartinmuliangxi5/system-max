"""
Streamlit 多页面应用示例 - 页面1
演示跨页面状态共享功能
"""

import streamlit as st
import streamlit_session_state_guide as guide


def page_one():
    st.title("📄 页面 1 - 跨页面状态共享演示")

    st.markdown("""
    ### 🔄 跨页面状态说明

    在这个多页面应用中，你可以看到：
    1. 在不同页面间导航时，状态如何保持
    2. 在此页面修改的状态如何在其他页面反映
    3. 导航历史如何追踪

    试试切换到页面2和页面3查看状态共享效果！
    """)

    # 初始化共享状态
    guide.CrossPageStateManager.init_shared_state()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("当前共享状态")
        shared = guide.CrossPageStateManager.get_shared_state()
        st.json(shared)

        # 添加导航记录
        guide.CrossPageStateManager.add_navigation_history("page_1")
        st.info(f"当前导航历史: {len(shared.get('navigation_history', []))} 次访问")

    with col2:
        st.subheader("状态操作")

        # 用户认证状态
        if shared.get('user_authenticated'):
            st.success(f"✅ 已登录: {shared.get('username')}")
            if st.button("退出登录"):
                st.session_state.user_authenticated = False
                st.session_state.username = None
                st.rerun()
        else:
            username = st.text_input("在此页面登录")
            if st.button("登录", key="login_page1"):
                st.session_state.user_authenticated = True
                st.session_state.username = username
                guide.CrossPageStateManager.add_navigation_history("login_from_page1")
                st.success(f"欢迎, {username}!")
                st.rerun()

        # 主题设置（跨页面生效）
        st.subheader("主题偏好")
        current_theme = shared.get('preferences', {}).get('theme', 'light')
        new_theme = st.selectbox(
            "选择主题",
            ['light', 'dark', 'auto'],
            index=['light', 'dark', 'auto'].index(current_theme) if current_theme in ['light', 'dark', 'auto'] else 0
        )
        if new_theme != current_theme:
            st.session_state.preferences['theme'] = new_theme
            st.success(f"主题已更改为 {new_theme} - 此更改将在所有页面生效!")
            st.rerun()

    st.divider()
    st.subheader("页面专用状态（不共享）")
    st.markdown("下面的状态仅在此页面存在，不会影响其他页面：")

    if 'page1_counter' not in st.session_state:
        st.session_state.page1_counter = 0

    st.metric("页面1计数器", st.session_state.page1_counter)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("增加计数"):
            st.session_state.page1_counter += 1
            st.rerun()
    with col2:
        if st.button("重置计数"):
            st.session_state.page1_counter = 0
            st.rerun()


if __name__ == "__main__":
    page_one()
