"""
Streamlit 多页面应用示例 - 页面3
演示跨页面状态共享功能
"""

import streamlit as st
import streamlit_session_state_guide as guide


def page_three():
    st.title("📄 页面 3 - 状态查看器")

    st.markdown("""
    ### 🔍 完整状态查看器

    此页面显示所有跨页面共享的完整状态，包括：
    - 用户认证信息
    - 购物车内容
    - 偏好设置
    - 导航历史

    你可以清楚地看到在其他页面所做的更改！
    """)

    # 初始化共享状态
    guide.CrossPageStateManager.init_shared_state()

    # 添加导航记录
    guide.CrossPageStateManager.add_navigation_history("page_3")

    shared = guide.CrossPageStateManager.get_shared_state()

    # 使用选项卡组织内容
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👤 用户信息", "🛒 购物车", "⚙️ 偏好设置", "📍 导航历史", "📊 统计"
    ])

    with tab1:
        st.subheader("用户认证状态")

        if shared.get('user_authenticated'):
            st.success("✅ 用户已登录")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("用户名", shared.get('username', 'N/A'))
            with col2:
                st.metric("登录状态", "已登录")

            if st.button("退出登录", key="logout_page3"):
                st.session_state.user_authenticated = False
                st.session_state.username = None
                st.success("已退出登录")
                st.rerun()
        else:
            st.warning("⚠️ 用户未登录")

            st.markdown("#### 在此页面登录：")
            username = st.text_input("用户名", key="login_page3")
            if st.button("登录", key="btn_login_page3"):
                st.session_state.user_authenticated = True
                st.session_state.username = username
                st.success(f"欢迎, {username}!")
                guide.CrossPageStateManager.add_navigation_history("login_from_page3")
                st.rerun()

    with tab2:
        st.subheader("购物车内容")

        cart_items = shared.get('cart_items', [])

        if cart_items:
            # 显示摘要
            total_items = sum(item['quantity'] for item in cart_items)
            total_price = sum(item['price'] * item['quantity'] for item in cart_items)

            col1, col2, col3 = st.columns(3)
            col1.metric("商品种类", len(cart_items))
            col2.metric("商品总数", total_items)
            col3.metric("总金额", f"¥{total_price:,.2f}")

            # 显示详细列表
            st.dataframe(
                cart_items,
                column_config={
                    'name': st.column_config.TextColumn('商品名称'),
                    'price': st.column_config.NumberColumn('单价', format='¥%.2f'),
                    'quantity': st.column_config.NumberColumn('数量'),
                    'category': st.column_config.TextColumn('类别'),
                    'added_at': st.column_config.TextColumn('添加时间')
                },
                hide_index=True
            )

            # 操作按钮
            col1, col2 = st.columns(2)
            with col1:
                if st.button("清空购物车", key="clear_cart_page3"):
                    st.session_state.cart_items = []
                    st.success("购物车已清空")
                    st.rerun()
            with col2:
                if st.button("结算 (演示)", key="checkout_page3"):
                    st.success("✅ 结算成功！感谢您的购买！")
                    st.session_state.cart_items = []
                    st.rerun()
        else:
            st.info("🛒 购物车是空的")
            st.markdown("前往 **页面2** 添加商品")

    with tab3:
        st.subheader("用户偏好设置")

        preferences = shared.get('preferences', {})

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 主题设置")
            current_theme = preferences.get('theme', 'light')
            theme_options = ['light', 'dark', 'auto']
            new_theme = st.selectbox(
                "主题",
                theme_options,
                index=theme_options.index(current_theme) if current_theme in theme_options else 0
            )
            if new_theme != current_theme:
                st.session_state.preferences['theme'] = new_theme
                st.success(f"主题已更新为 {new_theme}")
                st.rerun()

            st.markdown("#### 语言设置")
            current_lang = preferences.get('language', 'zh')
            lang_options = {'zh': '简体中文', 'en': 'English'}
            new_lang = st.selectbox(
                "语言",
                options=list(lang_options.keys()),
                format_func=lambda x: lang_options.get(x, x),
                index=list(lang_options.keys()).index(current_lang) if current_lang in lang_options else 0
            )
            if new_lang != current_lang:
                st.session_state.preferences['language'] = new_lang
                st.success(f"语言已更新为 {lang_options[new_lang]}")
                st.rerun()

        with col2:
            st.markdown("#### 当前设置")
            st.json(preferences)

    with tab4:
        st.subheader("导航历史")

        history = shared.get('navigation_history', [])

        if history:
            st.write(f"共 {len(history)} 次导航记录")

            # 按时间倒序显示
            for i, record in enumerate(reversed(history[-20:])):  # 只显示最近20条
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.write(record.get('page', 'unknown'))
                    with col2:
                        st.write(record.get('timestamp', ''))
                    with col3:
                        if st.button("清除", key=f"clear_nav_{i}"):
                            st.session_state.navigation_history.remove(record)
                            st.rerun()
        else:
            st.info("暂无导航记录")

        if st.button("清除所有导航历史"):
            st.session_state.navigation_history = []
            st.success("导航历史已清除")
            st.rerun()

    with tab5:
        st.subheader("统计信息")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "用户状态",
                "已登录" if shared.get('user_authenticated') else "未登录",
                delta="" if not shared.get('user_authenticated') else f"用户: {shared.get('username')}"
            )

        with col2:
            st.metric(
                "购物车",
                f"{len(shared.get('cart_items', []))} 件商品"
            )

        with col3:
            theme_icon = {"light": "☀️", "dark": "🌙", "auto": "🔄"}.get(
                shared.get('preferences', {}).get('theme', 'light'), "❓"
            )
            st.metric(
                "主题",
                f"{theme_icon} {shared.get('preferences', {}).get('theme', 'light').title()}"
            )

        with col4:
            st.metric(
                "导航次数",
                len(shared.get('navigation_history', []))
            )

        st.divider()
        st.subheader("完整共享状态JSON")
        st.json(shared)

    st.divider()
    st.info("💡 提示：试试修改此页面的设置，然后切换到其他页面查看效果！")


if __name__ == "__main__":
    # 修复 withst.container 写法错误
    page_three()
