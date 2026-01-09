# Job Bank

A Streamlit-based job search and application tracking tool that helps you find and manage job listings efficiently.

## Features

- **Job Search**: Search for jobs using custom queries via the JSearch API
- **Application Tracking**: Track the status of each job application (New, Applied, Interview, Offered, etc.)
- **Custom Queries**: Add and manage multiple job search queries
- **Filters**: Sort and filter job listings by status and company
- **Load More**: Efficiently load more jobs with pagination (up to 100 jobs per API call)
- **Google Authentication**: Secure login with Google OAuth
- **Per-User Settings**: API keys and preferences stored per user in MongoDB

## Tech Stack

- **Frontend**: Streamlit
- **Authentication**: Google OAuth via `streamlit-google-auth`
- **Database**: MongoDB
- **Job API**: JSearch API (OpenWebNinja)

## Setup

### Prerequisites

- Python 3.8+
- MongoDB instance
- Google OAuth credentials
- JSearch API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/JonaBaron/job-finder.git
   cd job-finder
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your configuration:
   ```env
   COOKIE_SECRET=your_cookie_secret
   REDIRECT_URI=http://localhost:8501
   MONGODB_URI=your_mongodb_uri
   ```

4. Add your Google OAuth credentials in `google_credentials.json`

5. Run the app:
   ```bash
   streamlit run app.py
   ```

### Configuration

After logging in, configure your API keys in **Settings**:
- **JSearch API**: Get your key from [OpenWebNinja](https://www.openwebninja.com/jsearch)
- **MongoDB URI**: Get your connection string from [MongoDB Atlas](https://www.mongodb.com/)

## Usage

1. **Login**: Sign in with your Google account
2. **Add Queries**: Go to "My Queries" to add job search terms
3. **Browse Jobs**: View job listings organized by query
4. **Track Applications**: Update job status as you apply
5. **Load More**: Click "Load More Jobs" to fetch additional listings

## Project Structure

```
Job Finder/
├── app.py                 # Main entry point & login page
├── pages/
│   └── job_board.py       # Main job board page
├── components/
│   ├── job_card.py        # Job card display components
│   └── dialog.py          # Dialog components (settings, queries, info)
├── models/
│   └── job.py             # Job model and status definitions
├── utils/
│   ├── auth.py            # Authentication utilities
│   ├── db.py              # Database connection
│   ├── db_user.py         # User database operations
│   ├── db_job.py          # Job database operations
│   ├── job_finder.py      # JSearch API integration
│   └── session_helper.py  # Session state management
└── google_credentials.json # Google OAuth credentials (not in repo)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Jonathan Mehmannavaz**

- GitHub: [@JonaBaron](https://github.com/JonaBaron)
- LinkedIn: [Jonathan Mehmannavaz](https://www.linkedin.com/in/jonathan-mehmannavaz/)
- Website: [jonabaron.github.io](https://jonabaron.github.io/)

---

Copyright (c) 2025 Jonathan Mehmannavaz
