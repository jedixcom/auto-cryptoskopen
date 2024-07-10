#html_creation
import os
import re
import html
from utils import create_url_slug, generate_summary, remove_original_images

def create_single_article_html(article_data, base_dir, domain_name, stop_words):
    # Validate required fields
    required_fields = ['title', 'category', 'full_text', 'summary', 'tags', 'timestamp']
    for field in required_fields:
        if field not in article_data:
            raise ValueError(f"Missing required field: {field}")

    # Create slugs and local file path
    title_slug = create_url_slug(article_data['title'], stop_words)
    category_slug = article_data['category'].lower().rstrip('.')
    local_file_path = os.path.join(base_dir, f"category/{category_slug}", f"{title_slug}.html")

    # Ensure directory exists
    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

    # Clean the full text
    clean_full_text = remove_original_images(article_data['full_text'])

    # Escape special characters in summary
    escaped_summary = html.escape(article_data['summary'])

    try:
        with open(local_file_path, 'w') as file:
            file.write(f"""
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="language" content="Dutch">
    <title>{article_data['title']}</title>
    <link rel="canonical" href="{domain_name}/category/{category_slug}/{title_slug}.html" />
    <meta name="description" content="{escaped_summary}">
    <meta name="keywords" content="{', '.join(article_data['tags'])}">
    <meta name="rating" content="General">
    <meta name="author" content="Peter Oldenburger" />
    <meta name="publisher" content="Peter Oldenburger" />
    <meta name="copyright" content="Peter Oldenburger" />
    <meta name="distribution" content="Global">
    <meta name="revisit-after" content="3 days">
    <meta name="robots" content="index, follow">
    <meta name="googlebot" content="index, follow">
    <meta name="googlebot-news" content="index, follow">
    <meta name="format-detection" content="telephone=no">
    <!-- Open Graph / Facebook -->
    <meta property="og:image" content="{domain_name}/resources/logo.webp">
    <meta property="og:image:alt" content="{article_data['title']}">
    <meta property="og:image:type" content="image/jpeg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:secure_url" content="{domain_name}/resources/logo.webp">
    <meta property="og:image:secure" content="true">
    <meta property="og:site_name" content="{domain_name}">
    <meta property="og:locale" content="nl_NL">
    <meta property="og:locale:alternate" content="en_US">
    <meta property="og:title" content="{article_data['title']}">
    <meta property="og:description" content="{escaped_summary}">
    <meta property="og:url" content="{domain_name}/category/{category_slug}/{title_slug}.html"/>
    <meta property="og:type" content="article">
    <meta property="article:published_time" content="{article_data['timestamp']}">
    <meta property="article:modified_time" content="{article_data['timestamp']}">
    <meta property="article:section" content="{article_data['category']}">
    <meta property="article:tag" content="{', '.join(article_data['tags'])}">
    <meta property="article:author" content="{domain_name}">
    <meta property="article:publisher" content="{domain_name}">
    <!-- Twitter -->
    <meta name="twitter:title" content="{article_data['title']}">
    <meta name="twitter:description" content="{escaped_summary}">
    <meta name="twitter:image" content="{domain_name}/resources/logo.webp">
    <meta name="twitter:image:alt" content="{article_data['title']}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@{domain_name}">
    <meta name="twitter:creator" content="@{domain_name}">
    <!-- Mobile Web App Meta Tags -->
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-title" content="{domain_name}">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <link rel="apple-touch-icon-precomposed" href="{domain_name}/resources/logo.webp">
    <link rel="shortcut icon" href="{domain_name}/resources/favicon.ico">
    <meta name="msapplication-navbutton-color" content="#006600">
    <meta name="application-name" content="CryptosKopen.eu - Cryptocurrency & Blockchain News">
    <meta name="msapplication-starturl" content="{domain_name}">
    <meta name="msapplication-window" content="width=1024;height=768">
    <meta name="msapplication-TileImage" content="{domain_name}/resources/logo.webp">
    <meta name="msapplication-TileColor" content="#006600">
    <meta name="theme-color" content="#ffffff">
    <link rel="icon" href="{domain_name}/resources/favicon.ico" type="image/x-icon">
    <link rel="apple-touch-icon" href="{domain_name}/resources/logo.webp">
    <link rel="manifest" href="{domain_name}/resources/manifest.json">
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        @media (max-width: 768px) {{
            .main-container {{
                flex-direction: column;
            }}
            .main-content, .sidebar {{
                width: 100%;
            }}
        }}
        body {{
            font-family: 'Poppins', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
        }}
        body, .main-container {{
            display: flex;
            flex-direction: column; 
        }}
        body .site-header {{
            width: 100%;
            top: 0; 
            position: relative; 
        }}
        header {{
            order: -1; 
        }}
        header {{
            background: #000000;
            color: #000;
            padding: 1rem 0;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        header .site-title {{
            color: #FFA500;
            font-weight: bold;
            text-decoration: none;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }}
        header h1 {{
            color: #000;
            font-weight: 900;
            font-size: 44px;
        }}
        h1 {{
            color: #000;
            font-size: 33px;
        }}
        footer {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f0f0f0;
            padding: 20px;
            opacity: 0; /* Initially hidden */
            transition: opacity 5s ease; /* Smooth transition */
        }}
        footer.visible {{
            opacity: 1; /* Show footer */
        }}
        .h1 {{
            font-size: 55px;
            font-weight: bold;
            text-decoration: none;
            background-color: #fff;
            color: #000;
            text-align: left;
            display: block;
        }}
        .h1:hover {{
            background-color: #000;
            color: #FFA500;
            text-decoration: none;
        }}
        h2 {{
            color: #000;
            font-size: 22px;
            font-weight: bold;
        }}
        .article h3 {{
            margin: 1rem 0;
            font-size: 1.5rem; /* Adjust font size as needed */
            font-weight: bold;
        }}
        .article h3 a {{
            color: #fff; /* Ensures the text is black */
            text-decoration: none;
        }}
        .article h3 a:hover {{
            color: #FFA500; /* Change color to red on hover */
        }}
        .article-container {{
            background: #fff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }}
        .full-text {{
            max-height: none; /* Remove any height limit */
            overflow: visible; /* Ensure text is not cut off */
        }}
        .navbar {{
            width: 100%;
            justify-content: center;
        }}
        .navbar-toggler {{
            margin-left: auto;
            margin-right: auto;
        }}
        .navbar-toggler {{
            margin-left: auto;
            margin-right: auto;
        }}
        .navbar-collapse {{
            justify-content: center;
            display: flex;
            width: 100%;
        }}
        .navbar-nav {{
            flex-direction: column;
            align-items: center;
            width: 100%;
        }}
        .navbar-nav .nav-link {{
            color: #000;
            padding: 0.5rem;
            width: 100%;
            text-align: center;
        }}
        .dropdown-menu {{
            text-align: center;
            width: 100%;
        }}
        @media (min-width: 992px) {{
            .navbar-nav {{
                flex-direction: row;
                justify-content: center;
            }}
        }}
        .navbar-nav .nav-item .nav-link {{
            color: #000;
            font-weight: 500;
        }}
        .navbar-nav .nav-item .nav-link:hover {{
            color: #FFA500;
        }}
        .main-container {{
            display: flex;
            flex-direction: column;
            max-width: 1000px;
            margin: 2rem auto;
            padding: 0 1rem;
        }}
        .main-content {{
            flex: 3;
            margin-right: 2rem;
        }}
        .sidebar {{
            flex: 1;
        }}
        .read-more {{
            width: 100%;
            padding: 0.5rem;
            margin-top: 0.5rem;
            border: none;
            border-radius: 5px;
            background-color: #000;
            color: #fff;
            font-weight: bold;
            text-align: left;
            text-decoration: none;
            font-size: 1.2rem;
            display: block;
        }}
        .widget {{
            margin-bottom: 2rem;
            background: #fff;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        .widget-title {{
            font-weight: bold;
            margin-bottom: 1rem;
            text-align: center;
        }}
        .search-bar input[type="text"] {{
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #ccc;
            border-radius: 5px;
        }}
        .search-bar button {{
            width: 100%;
            padding: 0.5rem;
            margin-top: 0.5rem;
            border: none;
            border-radius: 5px;
            background-color: #000000;
            color: white;
            font-weight: bold;
        }}
        .search-bar button:hover {{
            background-color: #000;
            color: #FFA500;
            text-decoration: none;
        }}
        .widget_recent_entries ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        .widget_recent_entries ul li {{
            display: flex;
            align-items: center;
            margin-bottom: 0.5rem;
            padding: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 5px;
            color: #000; /* Ensures the text is black */
        }}
        .widget_recent_entries ul li a {{
            color: #000; /* Ensures the text is black */
            text-decoration: none;
            flex: 1;
            font-size: 14px;
        }}
        .widget_recent_entries ul li img {{
            width: 50px;
            height: auto;
            margin-right: 10px;
            border-radius: 5px;
        }}
        .widget_recent_entries ul li a:hover {{
            text-decoration: none;
            color: #FFA500;
        }}
        .navbar .navbar-nav .nav-item {{
            position: center;
        }}
        .navbar .navbar-nav .nav-item .dropdown-menu {{
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            background-color: #FFA500;
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
            z-index: 1;
        }}
        .navbar .navbar-nav .nav-item:hover .dropdown-menu {{
            display: block;
        }}
        .navbar .navbar-nav .dropdown-menu li {{
            padding: 8px 16px;
            text-decoration: none;
            display: block;
        }}
        .navbar .navbar-nav .dropdown-menu li a {{
            color: black;
            text-decoration: none; /* Removes underline from links */
        }}
        .navbar .navbar-nav .dropdown-menu li a:hover {{
            background-color: #ddd; /* Gray background on hover */
        }}
        .share-options {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 1rem;
        }}
        .share-options a {{
            display: inline-block;
            width: 30px;
            height: 30px;
            background-color: #ddd;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            text-decoration: none;
            color: #333;
        }}
        .share-options a img {{
            width: 15px;
            height: 15px;
        }}
        .footer {{
            padding: 1rem;
            text-align: center;
            background: #000;
            color: #FFA500;
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
            margin-top: 2rem;
            flex-direction: column;
        }}
        .footer .footer-links a {{
            color: #fff;
            text-decoration: none;
            margin: 0 10px;
        }}
        .footer .footer-links a:hover {{
            color: #FFA500;
            text-decoration: none;
        }}
        .article {{
            background-color: #fff;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center; /* Center the content horizontally */
        }}
        .article h2 a {{
            color: #fff; /* Ensures the text is black */
            text-decoration: none;
        }}
        .article h2 a:hover {{
            color: #FFA500; /* Change color to red on hover */
            text-decoration: none;
        }}
        .widget_recent_entries {{
            margin-bottom: 2rem;
            background: #fff;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        .content-block {{
            display: none;
        }}
        @media (min-width: 768px) {{
            .main-container {{
                flex-direction: row;
            }}
            .main-content {{
                margin-right: 1rem;     
            }}
        }}
    </style>
</head>
<body>
    <header class="site-header">
        <img src="https://cryptoskopen.eu/resources/logo.webp" alt="headlinesmagazine news logo" style="width: 3.5%;">
        <a href="https://cryptoskopen.eu" class="site-title">CryptosKopen.EU - InSider Nieuws</a>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-center" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="/category/technology">Technology</a></li>
                    <li class="nav-item"><a class="nav-link" href="/category/cryptocurrency">Cryptocurrency</a></li>
                    <li class="nav-item"><a class="nav-link" href="/category/blockchain">Blockchain</a></li>
                    <li class="nav-item"><a class="nav-link" href="/category/finance">Finance</a></li>
                    <li class="nav-item"><a class="nav-link" href="/category/bitcoin">Bitcoin</a></li>
                    <li class="nav-item"><a class="nav-link" href="/category/hacking">Hacking</a></li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="aboutDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">About</a>
                        <div class="dropdown-menu text-center" aria-labelledby="aboutDropdown">
                            <a class="dropdown-item" href="/privacy-policy">Privacy Policy</a>
                            <a class="dropdown-item" href="/terms-of-service">Terms of Service</a>
                            <a class="dropdown-item" href="/disclaimer">Disclaimer</a>
                            <a class="dropdown-item" href="/contact">Contact</a>
                        </div>
                    </li>
                </ul>
            </div>
        </nav>
    </header>

    <div class="main-container">
        <div class="main-content">
            <div class="article-container">
                <h2>{article_data['title'] }</h2>
                <p><strong>Published on:</strong> { article_data['timestamp'] }</p>
                <p><strong>Author:</strong> DutchJinn @ CryptosKopen.EU 2024 copyright</p>
                <br>
                <div class="full-text">
                    <p>{ clean_full_text }</p>
                </div>
                <div class="share-options">
                    <a href="https://www.facebook.com/sharer/sharer.php?u={{ encodeURIComponent(window.location.href) }}" target="_blank" title="Share on Facebook"><img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" alt="Facebook" rel="nofollow"></a>
                    <a href="https://www.instagram.com/?url={{ encodeURIComponent(window.location.href) }}" target="_blank" title="Share on Instagram"><img src="https://cdn-icons-png.flaticon.com/512/733/733558.png" alt="Instagram" rel="nofollow"></a>
                    <a href="https://twitter.com/intent/tweet?url={{ encodeURIComponent(window.location.href) }}" target="_blank" title="Share on Twitter"><img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" alt="Twitter" rel="nofollow"></a>
                    <a href="https://pinterest.com/pin/create/button/?url={{ encodeURIComponent(window.location.href) }}" target="_blank" title="Share on Pinterest"><img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" alt="Pinterest" rel="nofollow"></a>
                    <a href="https://www.linkedin.com/sharing/share-offsite/?url={{ encodeURIComponent(window.location.href) }}" target="_blank" title="Share on LinkedIn"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" rel="nofollow"></a>
                    <a href="https://www.tumblr.com/widgets/share/tool?canonicalUrl={{ encodeURIComponent(window.location.href) }}" target="_blank" title="Share on Tumblr"><img src="https://cdn-icons-png.flaticon.com/512/733/733635.png" alt="Tumblr" rel="nofollow"></a>
                    <a href="https://www.reddit.com/submit?url={{ encodeURIComponent(window.location.href) }}" target="_blank" title="Share on Reddit" rel="nofollow"><img src="https://cdn-icons-png.flaticon.com/512/733/733609.png" alt="Reddit"></a>
                </div>
            </div>
        </div>
        <aside class="sidebar">
            <!-- Recent Posts -->
            <div id="recent-posts-2" class="widget widget_recent_entries">
                <h3 class="widget-title">Recent Posts</h3>
                <ul id="recent-posts-list">
                    <!-- Recent posts will be injected here -->
                </ul>
            </div>
            <!-- Tags Sidebar -->
            <div id="tag-sidebar" class="widget widget_tags">
                <h3 class="widget-title">Tags</h3>
                <ul>
                    <!-- Tags will be injected here -->
                </ul>
            </div>
            <!-- Categories -->
            <div id="categories-2" class="widget widget_categories">
                <h3 class="widget-title">Categories</h3>
                <ul>
                    <li><a href="/cryptocurrency">Cryptocurrency</a></li>
                    <li><a href="/finance">Finance</a></li>
                    <li><a href="/technology">Technology</a></li>
                    <li><a href="/blockchain">Blockchain</a></li>
                    <li><a href="/crypto">Crypto</a></li>
                    <li><a href="/bitcoin">Bitcoin</a></li>
                    <li><a href="/ethereum">Ethereum</a></li>
                    <li><a href="/nft">NFT</a></li>
                    <li><a href="/crypto-news">Crypto News</a></li>
                    <li><a href="/crypto-markets">Crypto Markets</a></li>
                    <li><a href="/crypto-trading">Crypto Trading</a></li>
                    <li><a href="/crypto-exchanges">Crypto Exchanges</a></li>
                    <li><a href="/crypto-wallets">Crypto Wallets</a></li>
                    <li><a href="/crypto-mining">Crypto Mining</a></li>
                    <li><a href="/crypto-stocks">Crypto Stocks</a></li>
                    <li><a href="/crypto-funds">Crypto Funds</a></li>
                    <li><a href="/crypto-investments">Crypto Investments</a></li>
                    <li><a href="/crypto-trading-strategies">Crypto Trading Strategies</a></li>
                    <li><a href="/crypto-trading-platforms">Crypto Trading Platforms</a></li>
                    <li><a href="/crypto-trading-algorithms">Crypto Trading Algorithms</a></li>
                    <li><a href="/crypto-trading-bots">Crypto Trading Bots</a></li>
                </ul>
            </div>
        </aside>
    </div>

    <footer class="footer">
        <div class="footer-links">
            <a href="/privacy-policy">Privacy Policy</a>
            <a href="/cookie-policy">Cookie Policy</a>
            <a href="/terms-of-service">Terms of Service</a>
            <a href="/avg">AVG</a>
            <a href="/gpdr">GPDR</a>
            <a href="/disclaimer">Disclaimer</a>
        </div>
    </footer>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
    <script>
        window.addEventListener('scroll', function () {{
            const scrollY = window.scrollY;
            if (scrollY > 50) {{
                document.querySelector('footer').classList.add('visible');
            }} else {{
                document.querySelector('footer').classList.remove('visible');
            }}
        }});
    </script>
    <script>
        async function loadRecentPostsAndTags() {{
            try {{
                const response = await fetch('https://cryptoskopen-eu-e5c24094abb7.herokuapp.com/get-blogs');
                const blogs = await response.json();
                const recentPostsList = document.getElementById('recent-posts-list');
                const tagsList = document.getElementById('tag-sidebar').querySelector('ul');

                blogs.sort((a, b) => new Date(b.date) - new Date(a.date));

                // Display recent posts
                blogs.slice(0, 5).forEach((blog) => {{
                    const recentPostItem = document.createElement('li');
                    recentPostItem.innerHTML = `
                        ${{blog.image_url ? `<img src="${{blog.image_url}}" alt="${{blog.title}}" style="width: 50px; height: auto; margin-right: 10px; border-radius: 5px;">` : ''}}
                        <a href="/category/${{blog.category.toLowerCase()}}/${{blog.slug}}.html">${{blog.title}}</a>
                    `;
                    recentPostsList.appendChild(recentPostItem);
                }});

                // Display tags
                const uniqueTags = new Set();
                blogs.forEach(blog => {{
                    blog.tags.forEach(tag => uniqueTags.add(tag));
               }});

                uniqueTags.forEach(tag => {{
                    const tagItem = document.createElement('li');
                    tagItem.innerHTML = `<a href="/tags/${{tag.toLowerCase().replace(/\s+/g, '-')}}">${{tag}}</a>`;
                    tagsList.appendChild(tagItem);
                }});
            }} catch (error) {{
                console.error('Error loading blogs:', error);
            }}
        }}

        loadRecentPostsAndTags();
    </script>
</body>
</html>
""")
        print(f"Local HTML file created at: {local_file_path}")
        return local_file_path

    except Exception as e:
        print(f"Failed to create HTML file: {str(e)}")
        return None