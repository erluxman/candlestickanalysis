from docx import Document
from docx.shared import Inches
import requests
import packaging.version
from io import BytesIO
from docx.shared import RGBColor
import os
import matplotlib.pyplot as plt

dummy_img_url = "https://media.istockphoto.com/id/117247268/photo/growth-chart.jpg?s=612x612&w=0&k=20&c=DokCI-1Ury3g02MwsRY_4NLX6ytKCL7zdXviJD2rVxo="


def write_dummy_docx():

    # Create a new Document object
    doc = Document()

    # Add a heading
    doc.add_heading("Document Title", 0)

    # Add a paragraph
    doc.add_paragraph("This is a simple paragraph.")

    # Add a bulleted list
    doc.add_paragraph("First item in the list", style="List Bullet")
    doc.add_paragraph("Second item in the list", style="List Bullet")

    # Add a numbered list
    doc.add_paragraph("First item in the numbered list", style="List Number")
    doc.add_paragraph("Second item in the numbered list", style="List Number")

    # Add a table
    table = doc.add_table(rows=2, cols=2)
    table.style = "Table Grid"  # Apply a style with borders
    cell_00 = table.cell(0, 0)
    cell_00.text = "Name"
    run_00 = cell_00.paragraphs[0].runs[0]
    run_00.bold = True
    run_00.font.color.rgb = RGBColor(255, 0, 0)  # Set text color to red

    cell_01 = table.cell(0, 1)
    cell_01.text = "Age"
    run_01 = cell_01.paragraphs[0].runs[0]
    run_01.bold = True
    run_01.font.color.rgb = RGBColor(255, 0, 0)  # Set text color to red

    table.cell(1, 0).text = "John Doe"
    table.cell(1, 1).text = "30"

    # Add an image from URL
    response = requests.get(dummy_img_url)
    img = BytesIO(response.content)
    doc.add_picture(img, width=Inches(4.0))

    # Generate and add a pie chart
    labels = "A", "B", "C", "D"
    sizes = [15, 30, 45, 10]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    pie_chart = BytesIO()
    plt.savefig(pie_chart, format="png")
    pie_chart.seek(0)
    doc.add_picture(pie_chart, width=Inches(4.0))
    plt.close(fig1)

    # Generate and add a scatter plot
    x = [1, 2, 3, 4, 5]
    y = [10, 20, 25, 30, 40]
    fig2, ax2 = plt.subplots()
    ax2.scatter(x, y)
    scatter_plot = BytesIO()
    plt.savefig(scatter_plot, format="png")
    scatter_plot.seek(0)
    doc.add_picture(scatter_plot, width=Inches(4.0))
    plt.close(fig2)

    # Generate and add a box plot
    data = [20, 30, 40, 50, 60, 70, 80, 90, 100]
    fig3, ax3 = plt.subplots()
    ax3.boxplot(data)
    box_plot = BytesIO()
    plt.savefig(box_plot, format="png")
    box_plot.seek(0)
    doc.add_picture(box_plot, width=Inches(4.0))
    plt.close(fig3)

    # Add dummy text for references
    # Create a new Document object for references
    ref_doc = Document()

    # Add a heading for references
    ref_doc.add_heading("References", level=1)
    ref_doc.add_paragraph(
        "1. Author A. (Year). Title of the paper. Journal Name, Volume(Issue), pages."
    )
    ref_doc.add_paragraph("2. Author B. (Year). Title of the book. Publisher.")
    
    
    
    # Add a table to the main document
    table = doc.add_table(rows=3, cols=3)
    table.style = "Table Grid"
    for i in range(3):
        for j in range(3):
            table.cell(i, j).text = f"Row {i+1}, Col {j+1}"

    # Generate and add a line chart
    x = [1, 2, 3, 4, 5]
    y = [10, 20, 30, 40, 50]
    fig4, ax4 = plt.subplots()
    ax4.plot(x, y)
    line_chart = BytesIO()
    plt.savefig(line_chart, format="png")
    line_chart.seek(0)
    doc.add_picture(line_chart, width=Inches(4.0))
    plt.close(fig4)

    # Add a long table to the references document
    long_table = ref_doc.add_table(rows=21, cols=2)
    long_table.style = "Table Grid"
    long_table.cell(0, 0).text = "Index"
    long_table.cell(0, 1).text = "Description"
    for i in range(1, 21):
        long_table.cell(i, 0).text = str(i)
        long_table.cell(i, 1).text = f"Description for item {i}"

    # Save the references document
    reference_path = "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/src/steps/docx_output/thesis_reference.docx"
    ref_doc.save(reference_path)

        
    output_path = "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/src/steps/docx_output/thesis_analysis.docx"
    doc.save(output_path)
    
    # Read the references document
    with open(reference_path, "rb") as ref_file:
        ref_doc = Document(BytesIO(ref_file.read()))

    # Append references to the main document
    for element in ref_doc.element.body:
        doc.element.body.append(element)

    # Save the combined document
    doc.save(output_path)
    os.system(f"open {output_path}")
