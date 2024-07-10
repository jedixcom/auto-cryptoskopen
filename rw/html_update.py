import os
from html_utils import create_url_slug, generate_summary, remove_original_images

def update_category_index(category, base_dir, articles, domain_name):
    category_slug = category.lower().replace(" ", "-").replace(".", "")
    category_index_path = os.path.join(base_dir, f"category/{category_slug}/index.html")
    
    os.makedirs(os.path.dirname(category_index_path), exist_ok=True)
    
    with open(category_index_path, 'w') as file:
        file.write(f"""
<!DOCTYPE html>
<html lang="nl">
<head>
                   
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                   
    <meta name="language" content="NL">
    <title>{{category}} - CryptosKopen.eu</title>
    <meta name="description" content="Alle artikelen in de categorie {{category}} op CryptosKopen.eu.">
                   
    <link rel="canonical" href="{{domain_name}}/category/{{category}}/" />
                   
    <meta name="keywords" content="categorie {{category}}">
    <meta name="rating" content="General">
    <meta name="author" content="{domain_name}" />
    <meta name="publisher" content="{domain_name}" />
    <meta name="copyright" content="{{domain_name}}" />
                   
    <meta name="distribution" content="Global">
    <meta name="revisit-after" content="3 days">
    <meta name="robots" content="index, follow">
    <meta name="googlebot" content="index, follow">
    <meta name="googlebot-news" content="index, follow">
    <meta name="format-detection" content="telephone=no">

    <!-- Open Graph / Facebook -->
    <meta property="og:image" content="{{domain_name}}/resources/logo.webp">
    <meta property="og:site_name" content="{{domain_name}}">

    <meta property="og:locale" content="nl_NL">
    <meta property="og:locale:alternate" content="en_US">

    <meta property="og:title" content="Category Items {{category}}">
    <meta property="og:description" content="Category Items {{category}}">
    <meta property="og:url" content="{domain_name}/category/{category_slug}"/>

    <meta property="og:type" content="website">

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
            font-size: 1.5rem;
            font-weight: bold;
        }}
        .article h3 a {{
            color: #fff;
            text-decoration: none;
        }}
        .article h3 a:hover {{
            color: #FFA500;
        }}
        .navbar {{
            width: 100%;
            justify-content: center;
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
            color: #000;
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
            position: relative;
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
    </style>
</head>
<body>
    <header class="site-header">
        <img src="https://cryptoskopen.eu/resources/logo.webp" alt="headlinesmagazine news logo" style="width: 3.5%;">
        <a href="https://cryptoskopen.eu" class="site-title">CryptosKopen.eu - InSider News</a>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-center" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="/technology">Technology</a></li>
                    <li class="nav-item"><a class="nav-link" href="/cryptocurrency">Cryptocurrency</a></li>
                    <li class="nav-item"><a class="nav-link" href="/bitcoin">Bitcoin</a></li>
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
    <div class="container">
        <h1 id="category-title">Artikelen</h1>
        <ul id="category-articles">
        </ul>
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
            <br><br>
            <p>&copy; 2024 CryptosKopen.eu</p>
        </div>
    </footer>

    <script>
        // Function to extract category from URL
        function getCategoryFromUrl() {{
            const pathParts = window.location.pathname.split('/');
            return pathParts[pathParts.length - 2]; // Assuming category is the second to last part of the URL
        }}

        async function loadCategoryArticles() {{
            try {{
                const category = getCategoryFromUrl();
                const response = await fetch(`https://cryptoskopen-eu-e5c24094abb7.herokuapp.com/get-blogs?category=${{category}}`);
                const blogs = await response.json();
                const articleList = document.getElementById('category-articles');
                const categoryTitle = document.getElementById('category-title');

                // Set the category title
                categoryTitle.textContent = `${{category.charAt(0).toUpperCase() + category.slice(1)}} Artikelen`;

                if (!articleList) {{
                    console.error('Article list element not found.');
                    return;
                }}

                blogs.forEach(blog => {{
                    const listItem = document.createElement('li');
                    const titleSlug = blog.slug;

                    listItem.innerHTML = `
                        <a href="/category/${{category}}/${{titleSlug}}.html">${{blog.title}}</a>
                    `;
                    articleList.appendChild(listItem);
                }});

                // Log a summary of articles fetched and rendered
                console.log(`Total number of articles fetched: ${{blogs.length}}`);
                console.log(`Total number of articles rendered: ${{articleList.querySelectorAll('li').length}}`);
            }} catch (error) {{
                console.error('Error loading category articles:', error);
                alert('Error loading category articles: ' + error.message);
            }}
        }}

        // Call the function to load category articles
        loadCategoryArticles();
    </script>
</body>
</html>
""")
    print(f"Category index updated at: {category_index_path}")

def update_index_html(rewritten_articles, base_dir, domain_name):
    index_html_path = os.path.join(base_dir, "blogx", "index.html")

    # Read the existing index HTML file
    with open(index_html_path, 'r') as file:
        index_html_content = file.read()

    # Define the markers to locate where to insert the articles
    articles_marker_start = "<!-- Articles will be injected here -->"
    articles_marker_end = "<!-- End of Articles -->"
    tags_marker_start = "<!-- Tags will be injected here -->"
    tags_marker_end = "<!-- End of Tags -->"
    categories_marker_start = "<!-- Categories will be injected here -->"
    categories_marker_end = "<!-- End of Categories -->"

    # Find the positions of the markers
    start_pos = index_html_content.find(articles_marker_start) + len(articles_marker_start)
    end_pos = index_html_content.find(articles_marker_end)
    tag_start_pos = index_html_content.find(tags_marker_start) + len(tags_marker_start)
    tag_end_pos = index_html_content.find(tags_marker_end)
    category_start_pos = index_html_content.find(categories_marker_start) + len(categories_marker_start)
    category_end_pos = index_html_content.find(categories_marker_end)

    # Extract existing sections
    existing_articles_html = index_html_content[start_pos:end_pos].strip()
    existing_tags_html = index_html_content[tag_start_pos:tag_end_pos].strip()
    existing_categories_html = index_html_content[category_start_pos:category_end_pos].strip()

    # Construct new HTML sections
    new_articles_html = ""
    new_tags_html = ""
    new_categories_html = ""
    tags_set = set()
    categories_dict = {}

    for article in rewritten_articles:
        summary = generate_summary(article['full_text'])  # Generate summary from full_text
        new_articles_html += f"""
            <div class="article">
                <h2>{article['title'][:60]}</h2>
                <p>{summary}</p>
                <a href="{article['url']}" class="read-more">Read More</a>
            </div>
        """
        # Collect tags
        for tag in article['tags']:
            tags_set.add(tag)

        # Collect categories and their articles
        category = article['category']
        if category not in categories_dict:
            categories_dict[category] = []
        categories_dict[category].append(article['title'])

    for tag in tags_set:
        new_tags_html += f'<li><a href="/tags/{tag.lower().replace(" ", "-")}">{tag}</a></li>'

    for category, titles in categories_dict.items():
        new_categories_html += f'<li><a href="/category/{category.lower().replace(" ", "-")}">{category}</a></li>'
        for title in titles:
            new_categories_html += f'<li class="subcategory">{title}</li>'

    # Update the index HTML content with the new articles, tags, and categories
    updated_index_html_content = (
        index_html_content[:start_pos] +
        "\n" + new_articles_html + "\n" +
        index_html_content[end_pos:tag_start_pos] +
        "\n" + new_tags_html + "\n" +
        index_html_content[tag_end_pos:category_start_pos] +
        "\n" + new_categories_html + "\n" +
        index_html_content[category_end_pos:]
    )

    # Write the updated index HTML file
    with open(index_html_path, 'w') as file:
        file.write(updated_index_html_content)

    print("Index HTML updated successfully.")