\# Issues Identified and Fixed



| \*\*Issue\*\* | \*\*Type\*\* | \*\*Line(s)\*\* | \*\*Description\*\* | \*\*Fix Approach\*\* |

|---|---|---|---|---|

| FTP usage | Security - High | 3, 68 | FTP was used for uploading reports, which is an insecure protocol. | Removed FTP and replaced the upload mechanism with HTTPS. |

| Unsafe deserialization | Security - Medium | 64 | `marshal.loads()` was used to deserialize stored application data. | Replaced `marshal` with JSON for storing and loading applications. |

| Hardcoded password | Security - Low | 67 | A bureau password was directly written in the source code. | Removed the hardcoded password and used the `BUREAU\_TOKEN` environment variable. |

| Insecure random generation | Security - Low | 51 | `random.randint()` was used to generate application IDs. | Replaced it with the `secrets` module. |

| Subprocess execution | Security - Low | 74 | `subprocess.run()` was used to launch a mail command. | Removed the subprocess call and changed the function to record a notification message. |

| Missing docstrings | Code Quality | Multiple | The module and several functions did not have proper documentation. | Added module and function docstrings. |

| Function naming convention | Code Quality | Multiple | Several function names did not follow the recommended `snake\_case` convention. | Renamed functions to follow the naming convention. |

| Mutable default argument | Code Quality | 20 | A mutable list was used as a default function argument. | Removed the mutable default argument. |

| Unused import | Code Quality | 2 | The `math` module was imported but was not used. | Removed the unused import. |

| Long lines and formatting | Style | Multiple | Several lines exceeded the allowed length and required formatting was missing. | Reformatted long lines and added proper spacing. |

