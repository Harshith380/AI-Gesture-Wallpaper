
from wallpaper_controller import WallpaperController


print("================================")
print(" WALLPAPER CONTROLLER TEST")
print("================================")

controller = WallpaperController()

print()

# Check categories
categories = controller.get_categories()

print("Available categories:")

for category in categories:
    print(f" - {category}")

print()

if not categories:
    print("No wallpaper categories found.")
    exit()

# -----------------------------------------
# TEST 1
# -----------------------------------------

print("TEST 1: Setting first wallpaper")

controller.set_wallpaper(0)

input(
    "\nPress ENTER to test next wallpaper..."
)


# -----------------------------------------
# TEST 2
# -----------------------------------------

print("\nTEST 2: Next wallpaper")

controller.next_wallpaper()

input(
    "\nPress ENTER to test next category..."
)


# -----------------------------------------
# TEST 3
# -----------------------------------------

print("\nTEST 3: Next category")

controller.next_category()

input(
    "\nPress ENTER to finish..."
)


print("\nWallpaper controller test completed.")

