import random
import string
from datetime import datetime


def generate_unique_filename(file_extension, length=10):
    characters = string.ascii_letters + string.digits
    random_sequence = ''.join(random.choice(characters) for _ in range(length))
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"{timestamp}_{random_sequence}{file_extension}"


def generate_posts(db, user, post):
    for i in range(20):
        new_post = post(
            title="Post Title " + str(i),
            content="<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras scelerisque enim ut nulla "
                    "sollicitudin, at bibendum mi auctor. Vivamus vitae lorem vitae ex ultricies posuere. Sed lacinia "
                    "enim vitae interdum scelerisque. Nullam sed enim ac odio placerat tristique. Nullam commodo elit "
                    "eu justo vulputate pellentesque. Donec consectetur vestibulum dui, nec bibendum enim commodo "
                    "sed. Duis sodales blandit ipsum mollis dapibus. Nullam quis mi quis nibh facilisis vehicula. In "
                    "lacinia mi id pharetra tristique. Pellentesque habitant morbi tristique senectus et netus et "
                    "malesuada fames ac turpis egestas. Vestibulum volutpat eu odio sit amet consequat.</p>"
                    "<p>Curabitur mauris ipsum, lacinia eget sagittis sagittis, porttitor sed diam. Nunc nec nunc "
                    "urna. Etiam porttitor consequat risus. Vivamus congue, velit a luctus gravida, arcu nunc "
                    "dignissim eros, eu commodo justo eros sit amet lectus. Cras cursus sem vitae purus condimentum, "
                    "vitae ullamcorper arcu mattis. Praesent at ipsum et nibh consectetur pretium. Suspendisse "
                    "pharetra quam eu mi ornare, eget eleifend sem laoreet. Etiam semper eros vel ex ultrices "
                    "condimentum. Etiam vehicula dolor purus, at volutpat turpis cursus eget. In sodales metus sit "
                    "amet lectus consectetur tincidunt ac eu nisl. Donec et ligula id dolor interdum ultricies.</p>"
                    "<p>Duis consectetur lacus nec erat cursus auctor. Lorem ipsum dolor sit amet, consectetur "
                    "adipiscing elit. Donec consequat augue nec ligula dignissim, eu ultrices nunc ornare. Curabitur "
                    "mattis mi.</p>"
            , status="active"
        )
        db.session.add(new_post)
        user.posts.append(new_post)
        db.session.commit()
