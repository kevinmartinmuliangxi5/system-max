"""
Streamlit 多页面应用示例 - 页面2
演示跨页面状态共享功能
"""

import streamlit as st
import streamlit_session_state_guide as guide


def page_two():
    st.title("📄 页面 2 - 购物车演示")

    st.markdown("""
    ### 🛒 跨页面购物车示例

    在此页面添加的商品会在所有其他页面中保留！
    试试添加商品，然后切换到页面3查看购物车状态。
    """)

    # 初始化共享状态
    guide.CrossPageStateManager.init_shared_state()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("添加商品")

        # 商品选择
        products = {
            '笔记本电脑': {'price': 5999, 'category': '电子产品'},
            '无线鼠标': {'price': 199, 'category': '电子产品'},
            '机械键盘': {'price': 399, 'category': '电子产品'},
            '显示器': {'price': 1299, 'category': '电子产品'},
            '笔记本支架': {'price': 99, 'category': '配件'},
            'USB-C 数据线': {'price': 49, 'category': '配件'},
        }

        with st.form("add_to_cart_form"):
            product = st.selectbox("选择商品", list(products.keys()))
            quantity = st.number_input("数量", min_value=1, max_value=10, value=1)
            submitted = st.form_submit_button("添加到购物车")

            if submitted:
                cart_item = {
                    'name': product,
                    'price': products[product]['price'],
                    'category': products[product]['category'],
                    'quantity': quantity,
                    'added_at': guide.datetime.now().isoformat()
                }
                st.session_state.cart_items.append(cart_item)
                guide.CrossPageStateManager.add_navigation_history("add_to_cart_page2")
                st.success(f"已添加 {quantity} 个 {product} 到购物车！")
                st.rerun()

    with col2:
        st.subheader("当前状态")

        shared = guide.CrossPageStateManager.get_shared_state()
        st.write(f"**购物车商品数:** {len(shared.get('cart_items', []))}")

        # 计算总价
        total = sum(
            item['price'] * item['quantity']
            for item in shared.get('cart_items', [])
        )
        st.metric("总价", f"¥{total:,.2f}")

        st.write(f"**用户状态:** {'已登录' if shared.get('user_authenticated') else '未登录'}")
        if shared.get('username'):
            st.write(f"**用户:** {shared.get('username')}")

        st.write(f"**主题:** {shared.get('preferences', {}).get('theme', 'light')}")

    st.divider()

    st.subheader("📦 当前购物车内容")

    cart_items = shared.get('cart_items', [])
    if cart_items:
        # 按类别分组显示
        by_category = {}
        for item in cart_items:
            cat = item['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(item)

        for category, items in by_category.items():
            with st.expander(f"{category} ({len(items)} 件商品)"):
                for i, item in enumerate(items):
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.write(item['name'])
                    with col2:
                        st.write(f"¥{item['price']}")
                    with col3:
                        st.write(f"x{item['quantity']}")
                    with col4:
                        if st.button("删除", key=f"remove_{category}_{i}"):
                            st.session_state.cart_items.remove(item)
                            st.rerun()

        # 清空购物车
        if st.button("🗑️ 清空购物车", type="secondary"):
            st.session_state.cart_items = []
            st.rerun()
    else:
        st.info("购物车是空的，添加一些商品吧！")


if __name__ == "__main__":
    page_two()
