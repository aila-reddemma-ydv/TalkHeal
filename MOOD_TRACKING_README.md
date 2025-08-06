# 📊 Mood Tracking Insights Dashboard

## Overview

The Mood Tracking Insights Dashboard is a comprehensive feature that allows users to track their emotional well-being over time, visualize patterns, and gain insights into their mental health journey.

## 🎯 Features

### 1. 📈 Mood History View
- **Line Chart**: Visual representation of mood progression over time
- **Bar Chart**: Distribution of different mood levels
- **Daily Summary**: Overview of mood by day with ratings
- **Filter Options**: 
  - Time period (7 days, 30 days, 90 days, all time)
  - Mood level filtering (Very Low, Low, Okay, Good, Great)

### 2. 📊 Analytics Dashboard
- **Key Metrics**:
  - Average mood score
  - Total mood entries
  - Most frequent mood
  - Mood range (highest to lowest)
- **Pattern Analysis**:
  - Mood by day of the week
  - Mood by time of day
  - Weekly trends

### 3. 💡 Insights & Reflections
- **Most Frequent Mood**: Identifies which mood appears most often
- **Trend Detection**: 
  - "Your mood has improved over the last 5 days"
  - "You've logged 'Sad' moods more frequently this week"
- **Contextual Insights**: Analyzes notes to find patterns
  - "You often feel anxious on Mondays"
  - "Positive mood is linked with outdoor activities"
- **Personalized Recommendations**: Based on average mood levels

## 🚀 How to Use

### Accessing the Dashboard
1. Open TalkHeal application
2. Look for the "📊 Mood Dashboard" button in the sidebar
3. Click to open the comprehensive mood tracking interface

### Tracking Your Mood
1. In the sidebar, expand "🧠 Mental Health Check"
2. Select your current mood level (😔 Very Low to 🌟 Great)
3. Add optional notes about your thoughts or feelings
4. Click "Get Tip & Save Entry" to save to the dashboard
5. View your entry in the dashboard immediately

### Navigating the Dashboard
The dashboard is organized into three main tabs:

#### 📈 Mood History Tab
- View your mood progression over time
- Use filters to focus on specific periods or mood levels
- See daily mood summaries
- Analyze mood distribution patterns

#### 📊 Analytics Tab
- Review key statistics about your mood patterns
- Explore how your mood varies by day of the week
- See time-of-day patterns in your emotional state
- Track your mood range and consistency

#### 💡 Insights Tab
- Get personalized insights about your mood patterns
- View trend analysis and improvements
- Read contextual insights from your notes
- Receive personalized recommendations

## 📊 Data Visualization

### Charts and Graphs
- **Line Charts**: Show mood progression over time
- **Bar Charts**: Display mood frequency distribution
- **Time-based Analysis**: Hourly and daily patterns
- **Weekly Patterns**: Day-of-week mood trends

### Interactive Features
- **Hover Information**: Detailed data on chart hover
- **Filter Controls**: Easy filtering by time and mood
- **Responsive Design**: Works on all screen sizes
- **Real-time Updates**: New entries appear immediately

## 🔒 Privacy & Data

### Data Storage
- All mood data is stored locally in `data/mood_data.json`
- No data is sent to external servers
- Your privacy is completely protected

### Data Structure
Each mood entry includes:
```json
{
  "timestamp": "2024-01-29T12:00:00",
  "mood_level": "good",
  "notes": "Optional notes about your mood",
  "date": "2024-01-29",
  "time": "12:00",
  "day_of_week": "Monday"
}
```

## 🎨 Mood Levels

The system uses a 5-point mood scale:
- **😔 Very Low (1)**: Extremely difficult day, may need support
- **😐 Low (2)**: Challenging but manageable
- **😊 Okay (3)**: Neutral, stable mood
- **😄 Good (4)**: Positive, enjoyable day
- **🌟 Great (5)**: Excellent, high-energy day

## 💭 Insights Examples

### Trend Detection
- "Your mood has improved by 1.2 points over the last week"
- "You've been consistently logging 'Good' moods on weekends"
- "Monday mornings tend to be your most challenging time"

### Contextual Patterns
- "You often feel better after outdoor activities"
- "Social interactions consistently improve your mood"
- "Work stress appears to impact your evening mood"

### Personalized Recommendations
- **For Low Average Mood**: Professional support suggestions
- **For Moderate Mood**: Self-care and habit-building tips
- **For High Average Mood**: Maintenance and goal-setting advice

## 🔧 Technical Details

### Dependencies
- `streamlit`: Web application framework
- `pandas`: Data manipulation and analysis
- `plotly`: Interactive charts and visualizations
- `json`: Data storage and retrieval

### File Structure
```
components/
├── mood_dashboard.py    # Main dashboard component
data/
├── mood_data.json      # User mood data storage
TalkHeal.py             # Main application (updated)
```

### Integration
The mood dashboard is fully integrated with:
- Existing mood tracking in sidebar
- Main application navigation
- Session state management
- Theme system

## 🎯 Benefits

### For Users
- **Self-Awareness**: Better understanding of emotional patterns
- **Progress Tracking**: Visual evidence of mood improvements
- **Pattern Recognition**: Identify triggers and positive influences
- **Motivation**: Celebrate positive trends and improvements
- **Support**: Personalized recommendations for challenging times

### For Mental Health
- **Early Detection**: Identify concerning patterns early
- **Treatment Support**: Data to share with healthcare providers
- **Coping Strategies**: Evidence-based recommendations
- **Prevention**: Proactive mood management

## 🚀 Future Enhancements

Potential future features:
- **Mood Triggers**: Tag specific events or activities
- **Correlation Analysis**: Link mood with sleep, exercise, etc.
- **Export Functionality**: Download mood data for external analysis
- **Reminder System**: Gentle prompts for mood tracking
- **Goal Setting**: Set mood improvement targets
- **Social Features**: Share progress with trusted contacts (optional)

## 📞 Support

If you encounter any issues with the mood tracking dashboard:
1. Check that all dependencies are installed
2. Verify the data directory exists and is writable
3. Restart the application if charts don't load
4. Check the browser console for any JavaScript errors

---

*The Mood Tracking Dashboard is designed to support your mental health journey with compassion and privacy. Remember, this tool is meant to complement, not replace, professional mental health care.*