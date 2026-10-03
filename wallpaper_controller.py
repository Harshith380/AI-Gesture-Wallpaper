
import os
import ctypes


class WallpaperController:

    def __init__(self, wallpaper_folder="wallpapers"):

        self.wallpaper_folder = wallpaper_folder

        # Category -> list of wallpaper paths
        self.categories = {}

        # Current category
        self.current_category = None

        # Current wallpaper index
        self.current_index = 0

        self.load_wallpapers()

    # ============================================================
    # LOAD WALLPAPERS
    # ============================================================

    def load_wallpapers(self):

        wallpaper_root = os.path.abspath(
            self.wallpaper_folder
        )

        print()
        print("Scanning wallpaper folder:")
        print(wallpaper_root)
        print()

        if not os.path.exists(wallpaper_root):

            print("ERROR: Wallpaper folder does not exist.")
            return

        supported_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".bmp",
            ".webp"
        }

        # Get category folders
        category_entries = os.scandir(
            wallpaper_root
        )

        for entry in category_entries:

            if not entry.is_dir():
                continue

            category_name = entry.name

            category_path = entry.path

            wallpapers = []

            # Scan files inside category
            try:

                for file_entry in os.scandir(
                    category_path
                ):

                    if not file_entry.is_file():
                        continue

                    extension = os.path.splitext(
                        file_entry.name
                    )[1].lower()

                    if extension in supported_extensions:

                        wallpapers.append(
                            os.path.abspath(
                                file_entry.path
                            )
                        )

            except OSError as error:

                print(
                    f"Could not read category "
                    f"{category_name}: {error}"
                )

                continue

            # Sort files alphabetically
            wallpapers.sort(
                key=lambda path: os.path.basename(
                    path
                ).lower()
            )

            # Add category if images exist
            if wallpapers:

                self.categories[
                    category_name
                ] = wallpapers

        # Sort categories alphabetically
        self.categories = dict(
            sorted(
                self.categories.items(),
                key=lambda item: item[0].lower()
            )
        )

        # ========================================================
        # DISPLAY RESULTS
        # ========================================================

        print("Wallpaper categories found:")

        if not self.categories:

            print("  No wallpaper categories found.")

            return

        for category, wallpapers in self.categories.items():

            print(
                f"  {category}: "
                f"{len(wallpapers)} wallpaper(s)"
            )

            for wallpaper in wallpapers:

                print(
                    f"      - "
                    f"{os.path.basename(wallpaper)}"
                )

        # ========================================================
        # SELECT FIRST CATEGORY
        # ========================================================

        category_list = list(
            self.categories.keys()
        )

        self.current_category = category_list[0]

        self.current_index = 0

        print()
        print(
            "Starting category:",
            self.current_category
        )

    # ============================================================
    # GET CURRENT CATEGORY
    # ============================================================

    def get_current_category(self):

        return self.current_category

    # ============================================================
    # GET CATEGORIES
    # ============================================================

    def get_categories(self):

        return list(
            self.categories.keys()
        )

    # ============================================================
    # SET CATEGORY
    # ============================================================

    def set_category(self, category):

        if category not in self.categories:

            print(
                f"ERROR: Category '{category}' "
                f"not found."
            )

            return

        self.current_category = category

        self.current_index = 0

        print()
        print(
            "================================"
        )

        print(
            f"Category changed to: {category}"
        )

        print(
            "================================"
        )

        self.set_wallpaper(0)

    # ============================================================
    # SET WALLPAPER
    # ============================================================

    def set_wallpaper(self, index):

        if self.current_category is None:

            print(
                "ERROR: No category selected."
            )

            return

        wallpapers = self.categories[
            self.current_category
        ]

        if not wallpapers:

            print(
                "ERROR: No wallpapers available."
            )

            return

        # Keep index within range
        index = index % len(wallpapers)

        wallpaper_path = wallpapers[index]

        try:

            result = ctypes.windll.user32.SystemParametersInfoW(
                20,
                0,
                wallpaper_path,
                3
            )

            if not result:

                print(
                    "ERROR: Windows could not "
                    "set the wallpaper."
                )

                return

            self.current_index = index

            print(
                "Wallpaper changed to:"
            )

            print(
                f"Category: "
                f"{self.current_category}"
            )

            print(
                f"Wallpaper: "
                f"{os.path.basename(wallpaper_path)}"
            )

        except Exception as error:

            print(
                f"ERROR: Could not change wallpaper: "
                f"{error}"
            )

    # ============================================================
    # NEXT WALLPAPER
    # ============================================================

    def next_wallpaper(self):

        if self.current_category is None:
            return

        wallpapers = self.categories[
            self.current_category
        ]

        if not wallpapers:
            return

        next_index = (
            self.current_index + 1
        ) % len(wallpapers)

        self.set_wallpaper(
            next_index
        )

    # ============================================================
    # PREVIOUS WALLPAPER
    # ============================================================

    def previous_wallpaper(self):

        if self.current_category is None:
            return

        wallpapers = self.categories[
            self.current_category
        ]

        if not wallpapers:
            return

        previous_index = (
            self.current_index - 1
        ) % len(wallpapers)

        self.set_wallpaper(
            previous_index
        )

    # ============================================================
    # NEXT CATEGORY
    # ============================================================

    def next_category(self):

        categories = self.get_categories()

        if not categories:
            return

        current_position = categories.index(
            self.current_category
        )

        next_position = (
            current_position + 1
        ) % len(categories)

        next_category = categories[
            next_position
        ]

        self.set_category(
            next_category
        )

    # ============================================================
    # PREVIOUS CATEGORY
    # ============================================================

    def previous_category(self):

        categories = self.get_categories()

        if not categories:
            return

        current_position = categories.index(
            self.current_category
        )

        previous_position = (
            current_position - 1
        ) % len(categories)

        previous_category = categories[
            previous_position
        ]

        self.set_category(
            previous_category
        )

