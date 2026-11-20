### Changed

- Community monitor: drops the claudelog source (its truncated changelog lines duplicate the changelog monitor), and a run that fetches no entries from any source, or leaves an empty report, now fails the job instead of opening an empty triage PR; the 70-odd uncovered tool names from the triage reports each get a recorded outcome (plan 0014 K27).
