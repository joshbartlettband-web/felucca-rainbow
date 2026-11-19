// SPDX-License-Identifier: GPL-3.0-only
package io.github.joshbartlettbandweb.fm1rescue.core;

/** A step that did not work. fatal: retrying cannot help (wrong chip, wrong package), so the app stops. */
public class RescueFail extends Exception {
    public final boolean fatal;

    public RescueFail(String msg) { this(msg, false); }

    public RescueFail(String msg, boolean fatal) {
        super(msg);
        this.fatal = fatal;
    }
}
