import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Grocery Invoice Generator", page_icon="🧾")

st.title("🧾 Grocery Shop Invoice Generator")

# --- Shop details ---
shop_name = st.text_input("Shop Name", "Rohan’s Grocery Store")
shop_address = st.text_area("Shop Address", "Pune, Maharashtra")
gst_rate = st.number_input("GST Rate (%)", value=5)

st.divider()

# --- Customer details ---
st.subheader("🧍 Customer Details")
customer_name = st.text_input("Customer Name")
customer_phone = st.text_input("Customer Phone")

st.divider()

# --- Item Entry Section ---
st.subheader("🛒 Add Items")

# ✅ Use a non-conflicting key name
if "invoice_items" not in st.session_state:
    st.session_state.invoice_items = []

with st.form("add_item_form"):
    col1, col2, col3 = st.columns(3)
    item_name = col1.text_input("Item Name")
    quantity = col2.number_input("Quantity", min_value=1, value=1)
    price = col3.number_input("Price (₹)", min_value=0.0, value=0.0)
    add_btn = st.form_submit_button("Add Item")

# ✅ Append new item to the correct list
if add_btn and item_name:
    st.session_state.invoice_items.append({
        "name": item_name,
        "quantity": quantity,
        "price": price
    })
    st.success(f"✅ Added {item_name}")

# --- Display Invoice ---
if st.session_state.invoice_items:
    st.subheader("🧾 Invoice Preview")

    invoice_no = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    st.write(f"**Invoice No:** {invoice_no}")
    st.write(f"**Date:** {datetime.now().strftime('%d-%m-%Y %H:%M')}")
    st.write(f"**Customer:** {customer_name or '-'}")
    st.write(f"**Phone:** {customer_phone or '-'}")

    st.markdown("---")
    st.write(f"**{shop_name}**")
    st.caption(shop_address)
    st.markdown("---")

    total = 0
    for idx, item in enumerate(st.session_state.invoice_items, start=1):
        amount = item["quantity"] * item["price"]
        total += amount
        st.write(f"{idx}. {item['name']} - {item['quantity']} × ₹{item['price']:.2f} = ₹{amount:.2f}")

    gst_amount = (gst_rate / 100) * total
    grand_total = total + gst_amount

    st.markdown("---")
    st.write(f"**Subtotal:** ₹{total:.2f}")
    st.write(f"**GST ({gst_rate}%):** ₹{gst_amount:.2f}")
    st.write(f"### 💰 Grand Total: ₹{grand_total:.2f}")
    st.markdown("---")

    st.info("📋 This is your invoice summary (not downloadable).")

    if st.button("🗑️ Clear All Items"):
        st.session_state.invoice_items = []
        st.success("All items cleared!")

else:
    st.info("Add items to generate your invoice.")
