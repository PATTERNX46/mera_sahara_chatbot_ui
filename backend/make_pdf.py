from fpdf import FPDF

# Create a PDF object
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# The content of our fake (but realistic) government scheme
scheme_content = """
GOVERNMENT OF INDIA - MINISTRY OF EDUCATION
Scheme Name: Bharat Vidyarthi Sahayak Yojana (BVSY) 2026

Objective: 
To provide financial assistance to meritorious students from economically weaker sections for higher education.

Eligibility Criteria:
1. The applicant must be a citizen of India.
2. The total annual family income from all sources must not exceed Rs. 3,00,000 (Three Lakh Rupees).
3. The student must be enrolled in a recognized Engineering, Medical, or Degree college.

Benefits Provided:
- Base Scholarship: Rs. 50,000 per year for tuition fees.
- Laptop Allowance: A one-time grant of Rs. 20,000 in the first year.

Special Provisions for Agricultural Families:
If the primary earner of the family is a registered farmer residing in the state of Bihar or Uttar Pradesh, the student is eligible for an additional "Krishi Bonus" of Rs. 15,000 per year to cover hostel and mess fees.

Application Deadline: 
All applications must be submitted via the Sarkari Sathi portal by October 31st, 2026.
"""

# Write the text to the PDF
pdf.multi_cell(0, 8, txt=scheme_content)

# Save the PDF to your backend folder
pdf.output("scheme.pdf")
print("✅ Successfully generated 'scheme.pdf' in your backend folder!")