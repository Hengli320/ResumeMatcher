from openai import OpenAI
import openai
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
system_content = ("I'll provide you with all the technical skills that a user has; along with a list of job objects. Each job object has 5 attributes: job_id, "
                  "job_title, company_name, job_link, job_requirements, and job_summary. I want you to act as a skill matcher to determine the most suitable job"
                  "given user's technical skills by comparing with job_requirements. Return a paragraph that list the most suitable job for the user. Please contain"
                  "the company_name, job_link, and a paragraph describe why the user is suitable for the job and what technical skills the user still missing for this job")


def generate_fit_paragraph(keywords, job_requirements):
    try:
        keywords_str = ", ".join(keywords) 
        job_requirements_str = "\n".join(
            f"Job ID: {job[0]}, Job Title: {job[1]}, Company: {job[2]}, Link: {job[3]}, Requirements: {', '.join(job[4])}, Summary: {job[5]}"
            for job in job_requirements
        )
        # Construct the message content
        user_content = f"User Skills: {keywords_str}\n\nJobs:\n{job_requirements_str}"
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error occured: {e}")

