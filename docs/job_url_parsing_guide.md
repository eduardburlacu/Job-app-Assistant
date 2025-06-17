# Job URL Parsing Guide

## How the URL Parser Works

The Job Application Assistant has an enhanced URL parser that can extract job information from various job sites. Here's how it works and how to get the best results:

## Supported Platforms

### ✅ Well Supported
- **Indeed** - Full extraction
- **Glassdoor** - Good extraction
- **Generic job sites** - Basic extraction

### ⚠️ Limited Support
- **LinkedIn** - Limited due to authentication requirements

## Using LinkedIn Job URLs

LinkedIn job URLs have limitations due to authentication requirements. Here's how to handle them:

### Option 1: Copy and Paste (Recommended)
1. Go to the LinkedIn job posting
2. **Copy the entire job description** from the page
3. In the app, select **"📝 Paste Text"**
4. Paste the job description
5. Click **"📋 Process Job Description"**

### Option 2: Manual Entry
1. Select **"✍️ Manual Entry"**
2. Fill in the job details manually:
   - Job Title
   - Company Name
   - Location
   - Requirements
   - Skills
   - Full Description

## What Gets Extracted

The parser automatically extracts:

- **Job Title** - The position name
- **Company Name** - The hiring company (NOT the job site name)
- **Location** - Job location or remote status
- **Requirements** - Key job requirements
- **Skills** - Technical skills mentioned
- **Employment Type** - Full-time, part-time, contract, etc.

## Tips for Best Results

### For LinkedIn:
- Copy the complete job description text
- Include company name, title, and full description
- Use the "Paste Text" option instead of URL

### For Other Sites:
- Use the direct job posting URL (not search results)
- Ensure the URL is publicly accessible
- If extraction fails, try copying the text instead

## Example Workflow

1. **Find the job** on LinkedIn/Indeed/etc.
2. **Try URL first** - If it works, great!
3. **If URL fails** - Copy the job description text
4. **Use "Paste Text"** option in the app
5. **Review extracted info** - Make sure it looks correct
6. **Proceed with application** generation

## Common Issues and Solutions

### "Unknown Company" or "Unknown Position"
- **Solution**: The site requires authentication or the format isn't recognized
- **Fix**: Copy the job description text and use "Paste Text" option

### Missing Requirements/Skills
- **Solution**: The job description might not have clear formatting
- **Fix**: Add missing information manually in the "Manual Entry" section

### LinkedIn Shows "LinkedIn" as Company
- **Solution**: This is a parsing limitation
- **Fix**: Use the "Paste Text" option instead of URL

## Getting Help

If you're having trouble with job extraction:
1. Try the "Paste Text" option instead of URL
2. Use "Manual Entry" for complete control
3. Check that the job posting is publicly accessible
4. Ensure the URL is for a specific job, not search results

The app is designed to be flexible - if one method doesn't work, try another approach!
