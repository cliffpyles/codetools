SYSTEM_CONTEXT = """
You are an expert at summarizing online content. You are able to summarize
information in a clear and concise manner without loosing any of the important
information.
"""

SUMMARY_PROMPT = """
Please utilize the following template to summarize the content you've just read. Your summary should accurately reflect the main ideas, key points, and any critical data presented in the content. Ensure that the essence and original message of the content are preserved, even in a condensed form. If the content involves arguments or discussions, capture the core thesis and provide a synopsis of the supporting arguments or counterarguments. Conclude with any final thoughts or conclusions drawn by the author. Remember to keep your summary clear, neutral, and devoid of personal opinions or interpretations.

# (Provide the title or headline of the content.)

## Summary
*A brief overview of the main points, findings, or storylines. This should be no more than a few sentences.*

### Steps Overview (Optional - exclude if not applicable)
*List the high-level steps involved in the tutorial or process-oriented content.*
- **Step 1:** Brief description
- **Step 2:** Brief description
- **Step 3:** Brief description
- *(Continue as necessary)*

## Key Highlights
*Bullet points of the most important facts, ideas, or themes presented.*
- **Highlight 1**
- **Highlight 2**
- **Highlight 3**
- *(Add more as necessary)*

## Visual Elements
*Note any significant visual elements included, such as images, charts, infographics, or videos.*

## Critical Analysis or Review (Optional - exclude if not applicable)
*A brief evaluation or critique of the content’s quality, relevance, and accuracy.*

## Implications/Impact
*Discuss the potential impact or significance of the content on its field, audience, or society.*

## Related Resources (Optional - exclude if not applicable)
*Links to related content or further reading/viewing/listening.*

## Personal Reflection/Action Points (Optional - exclude if not applicable)
*Personal takeaways, how the information might be used, or actions inspired by the content.*

## Content Details

| **Detail**          | **Information**                                      |
|---------------------|------------------------------------------------------|
| **Content Type**    | *e.g., blog post, video, podcast, news article, tutorial* |
| **Category**        | *Select the appropriate category*                    |
| **Subject Field**   | *Primary subject or field*                           |
| **Author/Creator**  | *Name of the individual or organization*             |
| **Source**          | *Publication, website, or platform*                  |
| **Publication Date**| *Date of publication or last update*                 |
| **URL**             | *Direct link*                                        |
| **Target Audience** | *Intended audience*                                  |

Ensure that your summary is concise yet comprehensive, providing a clear snapshot of the content's value and insights.
"""

CONTENT_TYPES = """
**News and Journalism**
- Breaking News
- Investigative Articles
- Feature Stories
- Opinion Pieces/Editorials
- News Analysis
- Press Releases

**Educational Content**
- How-to Guides and Tutorials
- Educational Articles and Essays
- Online Courses and Webinars
- E-books and Whitepapers
- Research Papers and Reports
- Case Studies

**Entertainment**
- Movie, Music, and Book Reviews
- Celebrity News and Gossip
- Satire and Humor Articles
- Comics and Graphic Novels
- Fan Fiction
- Podcasts and Web Series

**Lifestyle**
- Travel Blogs and Guides
- Food Recipes and Cooking Tips
- Fashion and Beauty Tips
- Health and Wellness Advice
- Personal Development and Self-Help
- Home Improvement and DIY Projects

**Technology**
- Tech News and Updates
- Product Reviews and Comparisons
- How-to Tech Guides
- Analysis and Opinion on Tech Trends
- Interviews with Industry Experts
- Cybersecurity Updates and Guides

**Business and Finance**
- Market Analysis and Financial News
- Business Strategy and Management Articles
- Investment Advice and Stock Market Tips
- Entrepreneurship and Startup Stories
- Case Studies and Business Profiles
- Personal Finance and Budgeting Tips

**Science and Environment**
- Scientific Discoveries and Research Summaries
- Environmental News and Sustainability Tips
- Wildlife Conservation Articles
- Space and Astronomy News
- Climate Change Reports and Analysis
- Health and Medical News

**Social Media and Blogging**
- Personal Blogs and Vlogs
- Influencer Content and Collaborations
- Social Media Updates and Trends
- Tutorials on Social Media Growth
- Commentary on Social Issues

**Creative Writing and Literature**
- Poetry and Short Stories
- Serialized Novels
- Literary Criticism and Analysis
- Writing Workshops and Tips
- Author Interviews and Biographies

**Sports and Recreation**
- Sports News and Commentary
- Game Previews and Recaps
- Player Interviews and Profiles
- Fantasy Sports Advice
- Outdoor Adventure and Travel

**Visual Content**
- Infographics and Data Visualizations
- Photo Essays
- Illustrations and Digital Art
- Video Content and Documentaries
- Virtual Reality Experiences

**Forums and Community Discussions**
- Q&A Sites
- Online Forums and Discussion Boards
- Comment Sections
- Social Media Groups and Threads
- Community Blogs and Wikis

**E-commerce and Marketing**
- Product Descriptions and Listings
- Marketing and Promotional Articles
- Customer Testimonials and Reviews
- Email Newsletters
- Affiliate Marketing Content

**Legal and Government**
- Legal Analysis and Commentary
- Government Policy Updates and Analysis
- Public Service Announcements
- Legal Documents and Forms
- Civic Engagement and Activism Articles
"""
