import streamlit as st
from typing import Dict, Any

st.set_page_config(page_title="GameMatch 🎮", layout="wide")

def init_session_state():
    if "page" not in st.session_state:
        st.session_state.page = "input"  # "input" or "results"
    if "matches" not in st.session_state:
        st.session_state.matches = {}    # from dummy backend
    if "ratings" not in st.session_state:
        st.session_state.ratings = {}    # match_id -> int rating

init_session_state()


# ----------------------------------------------------------------
# 1. Dummy backend fetcher
# ----------------------------------------------------------------
def dummy_fetch_matches() -> Dict[str, Dict[int, Any]]:
    """
    Simulate a backend response with two categories: my_community_matches & other_community_matches.
    """
    return {
        "my_community_matches": {
            111111: {
                "nickname": "Alice",
                "country": "USA",
                "platform": "steam",
                "library": {101,102},
                "achievements": {1,2,3},
                "game_similarity": 78,
                "achievement_similarity": 63
            },
            222222: {
                "nickname": "Bob",
                "country": "UK",
                "platform": "steam",
                "library": {201,202,203},
                "achievements": {7,8,9},
                "game_similarity": 85,
                "achievement_similarity": 90
            }
        },
        "other_community_matches": {
            333333: {
                "nickname": "Charlie",
                "country": "CAN",
                "platform": "xbox",
                "library": {300,301,302,303},
                "achievements": {5},
                "game_similarity": 60,
                "achievement_similarity": 45
            }
        }
    }


# ----------------------------------------------------------------
# 2. Input Page
# ----------------------------------------------------------------
def show_input_page():
    st.title("GameMatch 🎮")
    st.write("Discover Your Ultimate Gaming Companion.\n")

    platform = st.selectbox("Platform", ["steam", "xbox", "playstation"])
    user_id  = st.text_input("User ID:")

    st.write("**Similarity Preferences (0–100):**")
    game_pref = st.slider("Game Similarity", 0, 100, 50)
    ach_pref  = st.slider("Achievement Similarity", 0, 100, 50)

    # A single button to fetch matches
    if st.button("Find My Matches"):
        if not user_id.strip():
            st.error("Please enter a valid user ID.")
        else:
            # Simulate calling the backend
            st.session_state.matches = dummy_fetch_matches()
            st.session_state.page = "results"
            st.stop()


# ----------------------------------------------------------------
# 3. Results Page
# ----------------------------------------------------------------
def show_results_page():
    st.header("Your Match Results")
    matches = st.session_state.matches

    same_comm = matches.get("my_community_matches", {})
    diff_comm = matches.get("other_community_matches", {})

    st.subheader("Players in Your Community")
    if same_comm:
        for match_id, data in same_comm.items():
            render_match_card(match_id, data)
    else:
        st.info("No same-community matches found.")

    st.subheader("Players in Other Communities")
    if diff_comm:
        for match_id, data in diff_comm.items():
            render_match_card(match_id, data)
    else:
        st.info("No cross-community matches found.")

    # "Submit Ratings" if user has rated anything
    if st.session_state.ratings:
        if st.button("Submit All Ratings"):
            st.success("Ratings submitted!")
            st.session_state.ratings.clear()

    # A button to go back to the input page
    if st.button("Back to Input"):
        st.session_state.page = "input"
        st.stop()


def render_match_card(match_id: int, data: Dict[str, Any]):
    """
    Show a small block with match info + star rating (5 buttons).
    """
    st.write("---")
    nickname = data.get("nickname", "N/A")
    country  = data.get("country", "Unknown")
    g_sim    = data.get("game_similarity", 0)
    a_sim    = data.get("achievement_similarity", 0)
    library_size = len(data.get("library", []))
    achievements_size = len(data.get("achievements", []))

    # Basic info
    st.write(f"**{nickname}** ({country})")
    st.write(f"Games in Library: {library_size}")
    st.write(f"Achievements: {achievements_size}")
    st.write(f"Game Similarity: {g_sim}%")
    st.write(f"Achievement Similarity: {a_sim}%")

    # Star rating
    display_star_rating(match_id)


# ----------------------------------------------------------------
# 4. Star Rating Without Query Params
# ----------------------------------------------------------------
def display_star_rating(match_id: int):
    st.write("**Rate this match:**")
    current_rating = st.session_state.ratings.get(match_id, 0)

    columns = st.columns([5, 5, 5, 5, 100])
    for i in range(1, 6):
        star_symbol = "★" if i <= current_rating else "☆"
        with columns[i - 1]:
            if st.button(star_symbol, key=f"{match_id}_star_{i}"):
                st.session_state.ratings[match_id] = i

    # Display rating below
    if current_rating > 0:
        st.write(f"You rated this match {current_rating}/5")
    else:
        st.write("No rating yet.")






# ----------------------------------------------------------------
# 5. Main App
# ----------------------------------------------------------------
def main():
    if st.session_state.page == "input":
        show_input_page()
    else:
        show_results_page()

if __name__ == "__main__":
    main()
