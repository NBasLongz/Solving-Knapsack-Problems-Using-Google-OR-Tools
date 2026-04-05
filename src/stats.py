import os
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

def generate_summary():
    all_file = 'results/all_results.csv'
    
    if not os.path.exists(all_file):
        print(f" Không tìm thấy file {all_file}. Vui lòng chạy main.py trước.")
        return

    print(" Đang xử lý dữ liệu và tạo báo cáo...")

    # LOAD & PROCESS DATA
    df = pd.read_csv(all_file)
    
    if len(df) == 0:
        print(" File CSV rỗng.")
        return

    df['Is Optimal'] = df['Is Optimal'].astype(str).str.lower() == 'true'
    df['Total Value'] = pd.to_numeric(df['Total Value'], errors='coerce')
    df['Total Weight'] = pd.to_numeric(df['Total Weight'], errors='coerce')
    df['Solve Time (s)'] = pd.to_numeric(df['Solve Time (s)'], errors='coerce')

    summary_df = df.groupby('Group').agg(
        Num_Tests=('Instance', 'count'),
        Optimal_Percent=('Is Optimal', lambda x: x.mean() * 100),
        Avg_Time_s=('Solve Time (s)', 'mean'),
        Avg_Value=('Total Value', 'mean'),
        Avg_Weight=('Total Weight', 'mean')
    ).reset_index()

    summary_df = summary_df.round({'Optimal_Percent': 2, 'Avg_Time_s': 2, 'Avg_Value': 2, 'Avg_Weight': 2})

    summary_df = summary_df.sort_values(by=['Optimal_Percent', 'Avg_Time_s'], ascending=[False, True])
    
    summary_df.to_csv('Analysis/summary_stats.csv', index=False)

    top_k = min(3, len(summary_df))
    easy_groups = summary_df.head(top_k)['Group'].tolist()
    hard_groups = summary_df.tail(top_k)['Group'].tolist()

    # PLOT CHARTS
    plt.rcParams["figure.figsize"] = (10, 8)

    # Thời gian chạy
    plt.figure()
    plt.bar(summary_df["Group"], summary_df["Avg_Time_s"], color='salmon')
    plt.xticks(rotation=45)
    plt.ylabel("Seconds")
    plt.title("Average Solve Time per Group")
    plt.tight_layout()
    plt.savefig("Analysis/time_chart.pdf")
    plt.close()

    # Tỉ lệ tối ưu
    plt.figure()
    plt.bar(summary_df["Group"], summary_df["Optimal_Percent"], color='mediumseagreen')
    plt.xticks(rotation=45)
    plt.ylabel("Percentage (%)")
    plt.title("Optimal Rate per Group (%)")
    plt.tight_layout()
    plt.savefig("Analysis/optimal_chart.pdf")
    plt.close()

    pdf_path = "Analysis/BT4_Report.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Knapsack Experiment Report", styles["Title"]))
    content.append(Spacer(1, 20))

    content.append(Paragraph("1. Conclusion", styles["Heading2"]))
    content.append(Paragraph(
        f"<b>Easy groups</b> (High optimal %, fast solving): {', '.join(easy_groups)}", styles["Normal"]
    ))
    content.append(Paragraph(
        f"<b>Hard groups</b> (Low optimal %, slow solving): {', '.join(hard_groups)}", styles["Normal"]
    ))
    content.append(Paragraph(
        "<i>*Note: Time limit was set to 180 seconds per test case due to hardware limitations.</i>", styles["Normal"]
    ))
    content.append(Spacer(1, 20))

    # BẢNG THỐNG KÊ
    content.append(Paragraph("2. Summary Statistics Table", styles["Heading2"]))
    
    table_data = [summary_df.columns.tolist()] + summary_df.values.tolist()

    t = Table(table_data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    content.append(t)
    content.append(Spacer(1, 20))

    content.append(Paragraph("3. Visualization", styles["Heading2"]))
    content.append(Image("Analysis/optimal_chart.png", width=450, height=225))
    content.append(Spacer(1, 10))
    content.append(Image("Analysis/time_chart.png", width=450, height=225))

    doc.build(content)

    print("\n HOÀN TẤT! Đã tạo báo cáo thành công tại:")
    print(f" {pdf_path}")


if __name__ == "__main__":
    generate_summary()