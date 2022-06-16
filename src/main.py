
import os
debug = os.environ.get('DEBUG', False)

if debug:
    import debugpy

    debugpy.listen(5678)
    debugpy.wait_for_client()

from coco import main
main()