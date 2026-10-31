import streamlit as st
from src.analytics import METRICS, DIMENSIONS, aggregate, route_question
from src.generate_sales import generate_sales

st.set_page_config(page_title='AI 資料分析助理', page_icon='📊', layout='wide')

@st.cache_data
def load_data():
    return generate_sales()

sales = load_data()
st.title('📊 AI 資料分析助理')
st.caption('從商業問題到資料洞察 · 1,800 筆合成銷售資料 · 2025 年示範資料')
with st.sidebar:
    st.header('分析範圍')
    products = st.multiselect('產品', sorted(sales['product'].unique()), default=sorted(sales['product'].unique()))
    regions = st.multiselect('地區', sorted(sales['region'].unique()), default=sorted(sales['region'].unique()))
    months = st.slider('月份範圍', 1, 12, (1, 12))
    st.info('本示範以中英文關鍵字辨識問題，不使用大型語言模型；不需要 API 金鑰。')
frame = sales[sales['product'].isin(products) & sales['region'].isin(regions)
              & sales['date'].dt.month.between(*months)]
if frame.empty:
    st.warning('目前篩選沒有資料，請選擇至少一個產品與地區。')
    st.stop()
cols = st.columns(4)
for col, (label, value) in zip(cols, [('營收', frame.revenue.sum()), ('成本', frame.cost.sum()), ('毛利', frame.gross_profit.sum())]):
    col.metric(label, f'{value:,.0f}')
cols[3].metric('毛利率', f'{frame.gross_profit.sum() / frame.revenue.sum():.1%}')
st.caption(f'目前範圍：{len(frame):,} 筆交易；金額為示範用貨幣單位。所有結果皆套用左側篩選。')

examples = ['哪個產品營收最高？', '各地區營收', '每月銷售趨勢', '哪個產品毛利最高？']
st.subheader('提出分析問題')
for col, question in zip(st.columns(4), examples):
    if col.button(question, width='stretch'):
        st.session_state['question'] = question
with st.form('ask'):
    question = st.text_input('輸入中文或英文問題', key='question', placeholder='例如：Show revenue by region')
    submitted = st.form_submit_button('分析問題', type='primary')
# Input persists on reruns, keeping the selected analysis consistent with filters.
route = route_question(question)
if question.strip() and route is None:
    st.warning('目前支援產品、地區、月份的營收／成本／毛利分析。請使用上方範例，或下方手動選擇。')
if route:
    metric, dimension = route
    st.success(f'已辨識：依{DIMENSIONS[dimension]}分析{METRICS[metric]}')
else:
    left, right = st.columns(2)
    metric = left.selectbox('分析指標', list(METRICS), format_func=METRICS.get)
    dimension = right.selectbox('分析維度', list(DIMENSIONS), format_func=DIMENSIONS.get)
result = aggregate(frame, metric, dimension)
st.subheader(f'{DIMENSIONS[dimension]}{METRICS[metric]}分析')
if dimension != 'month':
    top = result.iloc[0]
    st.write(f'在目前範圍內，{top[dimension]} 的{METRICS[metric]}最高：{top[metric]:,.0f}。如有同額，請參閱下表。')
chart = result.set_index(dimension).rename(columns={metric: METRICS[metric]})
if dimension == 'month':
    st.line_chart(chart)
else:
    st.bar_chart(chart)
st.dataframe(result.rename(columns={dimension: DIMENSIONS[dimension], metric: METRICS[metric]}), hide_index=True, width='stretch')
st.download_button('下載分析結果 CSV', result.to_csv(index=False).encode('utf-8-sig'), 'analysis.csv', 'text/csv')
with st.expander('指標定義與資料明細'):
    st.markdown('營收 = 數量 × 單價；成本 = 數量 × 單位成本；毛利 = 營收 − 成本；毛利率 = 毛利 ÷ 營收。')
    st.dataframe(frame, hide_index=True, width='stretch')
    st.download_button('下載篩選後交易 CSV', frame.to_csv(index=False).encode('utf-8-sig'), 'sales.csv', 'text/csv')
st.caption('教學展示用途。資料於啟動時以固定 seed=7 產生，不含真實客戶或企業資料。')
