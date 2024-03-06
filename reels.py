import instaloader

def download_instagram_reels(urls):
    L = instaloader.Instaloader()

    for url in urls:
        try:
            post = instaloader.Post.from_shortcode(L.context, url.split('/')[-2])
            if post.is_video:
                L.download_post(post, target='reels')
                print(f"Reel downloaded successfully: {url}")
            else:
                print(f"Skipped non-video post: {url}")
        except Exception as e:
            print(f"Failed to download reel {url}: {e}")

if __name__ == "__main__":
    reels_urls = [
     #url list here  
    ]
    
    download_instagram_reels(reels_urls)

