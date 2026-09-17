import time
import random


# --- 1. USER CLASSES (Inheritance & Encapsulation) ---
class User:
    def __init__(self, username, user_type):
        self.username = username
        self.user_type = user_type
        self.__wallet = 0.0  # Private attribute (Encapsulation)

    def get_wallet_balance(self):
        return self.__wallet

    def add_funds(self, amount):
        self.__wallet += amount

    def deduct_funds(self, amount):
        if amount <= self.__wallet:
            self.__wallet -= amount
            return True
        return False


class BusinessOwner(User):
    def __init__(self, username, business_name, initial_budget):
        super().__init__(username, "Business Owner")
        self.business_name = business_name
        self.add_funds(initial_budget)
        self.my_campaigns = []

    def dashboard(self, app_system):
        while True:
            print(f"\n=== {self.business_name} Dashboard ===")
            print(f"Escrow Budget: {self.get_wallet_balance():.2f} PHP")
            print("1. Review Pending Submissions")
            print("2. Log Out")

            choice = input("Select an option: ")

            if choice == '1':
                self.review_submissions()
            elif choice == '2':
                break

    def review_submissions(self):
        print("\n--- Pending Submissions ---")
        has_pending = False
        for campaign in self.my_campaigns:
            for submission in campaign.submissions:
                if not submission.is_approved:
                    has_pending = True
                    print(f"\nCampaign: {campaign.title}")
                    print(f"Creator: {submission.creator.username}")
                    print(f"Link: {submission.link} | Views: {submission.views}")

                    approve = input("Approve and release payout? (y/n): ")
                    if approve.lower() == 'y':
                        # Calculate payout: 50 PHP per 1000 views
                        payout_multiplier = submission.views // 1000
                        total_payout = payout_multiplier * 50.0

                        if self.deduct_funds(total_payout):
                            submission.creator.add_funds(total_payout)
                            submission.is_approved = True
                            print(f"Success! {total_payout} PHP transferred to {submission.creator.username}.")
                        else:
                            print("Error: Insufficient budget in escrow.")

        if not has_pending:
            print("No pending submissions to review.")
        time.sleep(1)


class ContentCreator(User):
    def __init__(self, username):
        super().__init__(username, "Content Creator")

    def dashboard(self, app_system):
        while True:
            print(f"\n=== Creator Dashboard: {self.username} ===")
            print(f"Wallet Balance: {self.get_wallet_balance():.2f} PHP")
            print("1. Browse & Submit to Pabuya Campaigns")
            print("2. Log Out")

            choice = input("Select an option: ")

            if choice == '1':
                self.browse_campaigns(app_system)
            elif choice == '2':
                break

    def browse_campaigns(self, app_system):
        print("\n--- Active Local Campaigns ---")
        for idx, campaign in enumerate(app_system.active_campaigns):
            print(f"{idx + 1}. {campaign.title} by {campaign.owner.business_name} (Reward: 50 PHP / 1k views)")

        choice = input("\nEnter campaign number to submit work (or 0 to cancel): ")
        if choice.isdigit() and int(choice) > 0 and int(choice) <= len(app_system.active_campaigns):
            selected_campaign = app_system.active_campaigns[int(choice) - 1]
            link = input("Paste your video link: ")

            # Auto-generate a random view count between 1k and 15k
            views = random.randint(1000, 15000)
            print(f"Scanning link... Detected {views} views!")

            # Create a new Submission object
            new_sub = Submission(self, link, views)
            selected_campaign.add_submission(new_sub)
            print(f"Submission sent to {selected_campaign.owner.business_name} for review!")
            time.sleep(1)


# --- 2. SYSTEM CLASSES (Object Interaction) ---
class Campaign:
    def __init__(self, title, owner):
        self.title = title
        self.owner = owner
        self.submissions = []
        owner.my_campaigns.append(self)

    def add_submission(self, submission):
        self.submissions.append(submission)


class Submission:
    def __init__(self, creator, link, views):
        self.creator = creator
        self.link = link
        self.views = views
        self.is_approved = False


class PabuyaApp:
    def __init__(self):
        # Initialize mock database with a 4000 PHP budget for the business owner
        self.mock_owner = BusinessOwner("admin", "Kape Davao", 4000.00)
        self.mock_creator = ContentCreator("davao_vlogger")

        # Pre-load one campaign so the creator has something to interact with
        self.active_campaigns = [
            Campaign("Review our new Durian Coffee", self.mock_owner)
        ]

    def run(self):
        while True:
            print("\n" + "=" * 35)
            print(" Welcome to Pabuya App Prototype ")
            print("=" * 35)
            print("1. Log in as Kape Davao (Business)")
            print("2. Log in as davao_vlogger (Creator)")
            print("3. Exit")

            choice = input("Select user: ")

            if choice == '1':
                self.mock_owner.dashboard(self)
            elif choice == '2':
                self.mock_creator.dashboard(self)
            elif choice == '3':
                print("Closing system...")
                break
            else:
                print("Invalid input.")


if __name__ == "__main__":
    app = PabuyaApp()
    app.run()