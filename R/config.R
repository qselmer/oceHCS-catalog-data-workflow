# Project configuration helpers -------------------------------------------------

read_ocehcs_paths <- function(
  local_file = "config/paths.local.yml",
  example_file = "config/paths.example.yml"
) {
  if (!requireNamespace("yaml", quietly = TRUE)) {
    stop("Package 'yaml' is required.", call. = FALSE)
  }

  if (!file.exists(local_file)) {
    stop(
      "Missing local path configuration: ",
      local_file,
      ". Copy ",
      example_file,
      " to ",
      local_file,
      " and edit ocean_data_root for this machine.",
      call. = FALSE
    )
  }

  cfg <- yaml::read_yaml(local_file)

  if (
    is.null(cfg$ocean_data_root) ||
    !nzchar(cfg$ocean_data_root)
  ) {
    stop("'ocean_data_root' is not configured.", call. = FALSE)
  }

  root <- normalizePath(
    cfg$ocean_data_root,
    winslash = "/",
    mustWork = FALSE
  )

  rel <- cfg$paths

  out <- c(
    list(root = root),
    lapply(
      rel,
      function(x) file.path(root, x)
    )
  )

  class(out) <- c("ocehcs_paths", class(out))
  out
}

print.ocehcs_paths <- function(x, ...) {
  cat("oceHCS data root:\n  ", x$root, "\n", sep = "")
  invisible(x)
}
