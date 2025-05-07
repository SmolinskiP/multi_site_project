# Django Multi-Site Project

A Django project handling two separate domains in a single Django installation:
* **ashes.pl** - a fire performance group website
* **dailystoic.pl** - daily stoic quotes and wisdom

## Project Overview

This project demonstrates a multi-domain approach using Django's flexibility to serve completely different content on different domains with a single codebase. Each site has independent views, models, templates, and URLs while sharing common infrastructure.

## Site Features

### Ashes.pl
- Dynamic gallery with category filtering
- Workshop and fire show information pages
- Contact form with database storage
- Custom error pages (404, 500)

### DailyStoic.pl
- Daily automatic quote rotation
- Newsletter subscription system
- Automated email delivery for quotes
- Admin interface for quote management

## Technical Architecture

The project uses domain recognition middleware to determine which site configuration to load. Key components:

### Domain Recognition
- Custom middleware detects the current domain
- Sets appropriate URL configuration based on the domain
- Maintains separate page rendering logic for each site

### Data Models
- **Ashes**: Categories, GalleryImages, ContactMessages
- **DailyStoic**: Quotes, NewsletterSubscribers

### Shared Infrastructure
- Common admin panel
- Shared database
- Visit statistics tracking
- Error handling

## Implementation Details

### Domain Middleware
The middleware examines incoming requests and sets the correct URL configuration:

```python
class DomainMiddleware:
    def __call__(self, request):
        host = request.get_host().split(':')[0]
        
        if 'ashes.pl' in host:
            request.current_site = 'ashes'
            request.urlconf = 'multi_site_project.urls_ashes'
        elif 'dailystoic.pl' in host:
            request.current_site = 'dailystoic'
            request.urlconf = 'multi_site_project.urls_dailystoic'
        else:
            request.current_site = 'default'
```

### URL Configurations
Separate URL files for each domain:
- `urls_ashes.py` for ashes.pl
- `urls_dailystoic.py` for dailystoic.pl

### Models & Admin
Each site has dedicated models with specialized admin interfaces:

**Ashes Models:**
- Category - for organizing gallery content
- GalleryImage - for storing and displaying images
- ContactMessage - for handling contact form submissions

**DailyStoic Models:**
- Quote - for storing daily stoic quotes
- NewsletterSubscriber - for managing newsletter subscriptions

### Email Systems
The DailyStoic site includes:
- Automated newsletter delivery
- Welcome emails for new subscribers
- Unsubscribe functionality

## Development Notes

- Set up local domain testing by modifying your hosts file
- Each template set is completely independent
- Media files are shared between sites but organized in site-specific folders
- Admin interface provides access to both sites' data
- Visit statistics are tracked globally across both domains

## Technical Requirements

- Python 3.8+
- Django 4.2+
- PostgreSQL recommended
- Email service configuration required for DailyStoic functionality