### Changed

- The doc graph page is simpler and faster: docs only (no cited-domain nodes), live search that dims non-matching docs as you type (Enter zooms to the first match), one checkbox per topic hub plus "Unfiled" and "Select all", colour by top-level folder, and a click opens the doc on GitHub. Its JSON is a slim projection (`site_graph`: title, bucket, hubs, one edge per linked pair), and the Pages site now redeploys on every push to `main` (plan 0015 G2)
